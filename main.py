import os
from chat import Model
from chat import ChatSession

model = Model("gpt-3.5-turbo", 0, os.environ["OPENAI_KEY"])
chat = ChatSession(model)
print(chat("Hello there!"))
