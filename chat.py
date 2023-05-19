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
    def __init__(self, model: Model, system_prompt: str):
        self.model = model
        self.chat_messages = [ChatMessage("system", system_prompt)]

    def __call__(self, message: str):
        self.chat_messages.append(ChatMessage("user", message))
        response = self.model(self.chat_messages)
        self.chat_messages.append(ChatMessage("assistant", response))
        return response
