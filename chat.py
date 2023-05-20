import requests


class ChatMessage:
    def __init__(self, role: str, text: str):
        self.role = role
        self.text = text


class Model:
    def __init__(self, model_name: str, temperature: float, api_key: str):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key

    def __call__(self, messages: list[ChatMessage]):
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model_name,
                "temperature": self.temperature,
                "messages": [
                    {"role": message.role, "content": message.text}
                    for message in messages
                ],
            },
        )
        response = response.json()
        if "choices" not in response:
            raise ValueError(f"Response {response} does not contain choices.")
        if len(response["choices"]) != 1:
            raise ValueError(f"Response {response} contains more than one choice.")
        if "message" not in response["choices"][0]:
            raise ValueError(f"Response {response} does not contain a message.")
        if "content" not in response["choices"][0]["message"]:
            raise ValueError(f"Response {response} does not contain content.")
        return response["choices"][0]["message"]["content"]


class ChatSession:
    def __init__(self, model: Model, system_prompt: str, memory_length: int):
        self.model = model
        self.system_prompt = system_prompt
        self.chat_messages = []
        self.memory_length = memory_length

    def prune_messages(self):
        if self.memory_length > 0 and len(self.chat_messages) > self.memory_length:
            self.chat_messages = self.chat_messages[-self.memory_length :]
        elif self.memory_length == 0:
            self.chat_messages = []

    def __call__(self, message: str, prune_messages: bool = True):
        self.chat_messages.append(ChatMessage("user", message))
        final_chat_messages = [ChatMessage("system", self.system_prompt)]
        final_chat_messages.extend(self.chat_messages)
        response = self.model(final_chat_messages)
        self.chat_messages.append(ChatMessage("assistant", response))
        if prune_messages:
            self.prune_messages()
        return response
