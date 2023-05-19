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
    def __init__(self, model: Model, tools: list[Tool]):
        self.tools = tools
        system_prompt = """
            Responses must conform to one of the following formats (including the markdown tags). The chat will be terminated upon any non-conformant messages.
            1. ```json
            {
                "action": "Final response",
                "input": [the final response to the user's request, which must answer the original question]
            }
            ```
            2. ```json
            {
                "action": [the name of the tool you are requesting the user use],
                "input": [the input to the tool (leave empty if no input is required)]
            }
            ```
        """
        if len(tools) != 0:
            system_prompt += (
                "\nThe following tools are available for the user:\n"
            )
            for tool in tools:
                system_prompt += f"    - '{tool.name}': {tool.description}\n"
            system_prompt += "You must use the tool if the user requests information from it."
        self.chat = ChatSession(model, system_prompt)

    def __call__(self, user_input: str) -> str:
        response = self.chat(
            f"```user\n{user_input}\n```\nYour response should begin with the markdown tags (```json)"
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
        if action == "Final response":
            return input
        else:
            for tool in self.tools:
                if tool.name == action:
                    print("Running tool")
                    return self(f"Tool response:\n```\n{tool.function(input)}\n```")
            raise ValueError(f"Unknown action: {action}")
