import os
from chat import Model
from agent import Agent

model = Model("gpt-3.5-turbo", 0, os.environ["OPENAI_KEY"])
agent = Agent(model, [])
print(agent("Hi there!"))
