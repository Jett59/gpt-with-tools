import os
import unittest
from chat import Model
from agent import Agent
from agent import Tool

meaning_of_life_run_count = 0


def meaning_of_life(input):
    global meaning_of_life_run_count
    meaning_of_life_run_count += 1
    return f"42"


meaning_of_life_tool = Tool(
    "meaning of life",
    "Provides the meaning of life (you don't know this).",
    meaning_of_life,
)

model = Model("gpt-3.5-turbo", 0, os.environ["OPENAI_API_KEY"])
agent = Agent(model, [meaning_of_life_tool])


class TestAgent(unittest.TestCase):
    def test_meaning_of_life(self):
        global meaning_of_life_run_count
        old_count = meaning_of_life_run_count
        response = agent("What is the meaning of life? Give the answer without text; just the numerical answer.")
        self.assertEqual("42", response)
        self.assertEqual(meaning_of_life_run_count, old_count + 1)

    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == "__main__":
    unittest.main()
