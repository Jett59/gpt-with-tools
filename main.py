import os
from chat import Model
from chat import ChatMessage

model = Model("gpt-3.5-turbo", 0, os.environ["OPENAI_KEY"])
model([ChatMessage("system", "You are a helpful assistant.")])
