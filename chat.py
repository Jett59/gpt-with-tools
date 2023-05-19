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
        return response.json()["choices"][0]["message"]["content"]


class ChatSession:
    def __init__(self, model):
        self.model = model
        self.messages = []

    def __call__(self, message: str):
        self.messages.append(ChatMessage("user", message))
        response = self.model(self.messages)
        self.messages.append(ChatMessage("assistant", response))
        return response
