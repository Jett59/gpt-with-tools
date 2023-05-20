import os
from chat import Model
from agent import Agent
from agent import Tool


def list_directory(directory):
    print(directory)
    return os.listdir(directory)


model = Model("gpt-3.5-turbo", 0, os.environ["OPENAI_API_KEY"])
agent = Agent(
    model,
    [
        Tool(
            "list directory", "List the contents of the given directory", list_directory
        ),
    ],
    0,
)

while True:
    user_input = input("User: ")
    print("Assistant:", agent(user_input))
