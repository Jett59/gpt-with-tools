import os
from chat import Model
from agent import Agent
from agent import Tool


def list_directory(directory):
    return "Documents Downloads code"


model = Model("gpt-3.5-turbo", 0, os.environ["OPENAI_KEY"])
agent = Agent(model, [Tool("ls", "List the given directory", list_directory)])
print(agent("Hi there! What is in the /tmp directory?"))
