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
        if len(tools) == 0:
            system_prompt = "You are a helpful assistant."
        else:
            system_prompt = "You are a helpful assistant. You may request the following actions from the user:\n"
            for tool in tools:
                system_prompt += f"- {tool.name}: {tool.description}\n"
        system_prompt += """
            There are two formats for your response, both of which are formatted in markdown:
            1. ```json
            {
                "action": "Final response",
                "input": [the final response to the user's request]
            }
            ```
            2. ```json
            {
                "action": [the name of the action you are requesting from the user],
                "input": [the input to the action]
            }
            ```
        """
        self.chat = ChatSession(model, system_prompt)

    def __call__(self, user_input: str) -> str:
        response = self.chat(
            f"Don't forget to respond in the specified format. The user's message follows:\n{user_input}"
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
                    return tool.function(input)
            raise ValueError(f"Unknown action: {action}")
