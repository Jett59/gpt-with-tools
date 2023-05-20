import json
from typing import Callable

from chat import ChatSession
from chat import Model


class Tool:
    def __init__(self, name: str, description: str, function: Callable[[str], str]):
        self.name = name
        self.description = description
        self.function = function


class Agent:
    def __init__(self, model: Model, tools: list[Tool], memory_length: int = 0):
        self.tools = tools
        system_prompt = """
            Responses must conform to one of the following formats (including the markdown tags). The chat will be terminated upon any non-conformant messages.
            1. ```json
            {
                "action": "final response",
                "input": [the final response to the user's request, which must answer the original question]
            }
            ```
            2. ```json
            {
                "action": [the name of the tool you are requesting the user use, which must be one of the list below],
                "input": [the input to the tool (leave empty if no input is required)]
            }
            ```

            After a final response message, the user will be required to give another prompt.
        """
        if len(tools) != 0:
            system_prompt += "\nThe following tools are available for the user:\n"
            for tool in tools:
                system_prompt += f"    - '{tool.name}': {tool.description}\n"
            system_prompt += "You must not try to use a tool not listed here."
        self.chat = ChatSession(model, system_prompt, memory_length)

    def __call__(self, user_input: str, depth=0) -> str:
        if depth > 32:
            return "Looks like we got confused. Can you try something else?"

        response = self.chat(
            f"```user\n{user_input}\n```\nYour response must begin with ```json and end with ```.",
            False,
        )
        if not response.startswith("```json\n"):
            raise ValueError(f"Response {response} does not start with ```json\n.")
        response = response[len("```json\n") :]
        if not response.endswith("```"):
            raise ValueError(f"Response {response} does not end with ```.")
        response = response[: -len("```")]
        try:
            response = json.loads(response)
        except json.JSONDecodeError:
            raise ValueError(f"Response {response} is not valid JSON.")
        if "action" not in response:
            raise ValueError(f"Response {response} does not contain an action.")
        if "input" not in response:
            raise ValueError(f"Response {response} does not contain an input.")
        action = response["action"]
        input = response["input"]
        if action == "final response":
            # We do it manually here to avoid losing the messages from the tool responses.
            self.chat.prune_messages()
            return input
        else:
            for tool in self.tools:
                if tool.name == action:
                    print("Running tool")
                    try:
                        tool_response = tool.function(input)
                    except Exception as e:
                        return self(
                            f"An error occurred while running the tool:\n```\n{e}\n```",
                            depth=depth + 1,
                        )
                    if isinstance(tool_response, str):
                        formatted_tool_response = (
                            f"Tool response:\n```{tool_response}```\n"
                        )
                    elif isinstance(tool_response, list) or isinstance(
                        tool_response, dict
                    ):
                        formatted_tool_response = f"Tool response:\n```json\n{json.dumps(tool_response, indent=4)}\n```"
                    else:
                        raise ValueError(
                            f"Tool response {tool_response} is not a string, list or dictionary."
                        )
                    return self(formatted_tool_response, depth=depth + 1)
            raise ValueError(f"Unknown action: {action}")
