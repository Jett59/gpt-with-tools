import os
import unittest
from chat import Model
from agent import Agent
from agent import Tool


def meaning_of_life(input):
    return f"42"


meaning_of_life_tool = Tool("meaning of life", "Provides the meaning of life.", meaning_of_life)

model = Model("gpt-3.5-turbo", 0, os.environ["OPENAI_API_KEY"])
agent = Agent(model, [meaning_of_life_tool])


class TestAgent(unittest.TestCase):

    def test_meaning_of_life(self):
        response = agent("What is the meaning of life?")
        self.assertEqual('42', response)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
