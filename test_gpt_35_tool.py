import os
import unittest
from chat import Model
from agent import Agent
from agent import Tool

meaning_of_life_run_count = 0


def meaning_of_life(input):
    global meaning_of_life_run_count
    meaning_of_life_run_count += 1
    return {
        "meaning of life": 2138384
    }


meaning_of_life_tool = Tool("meaningOfLife", "Provides the meaning of life. You do not know the meaning of life. If asked anything about the meaning of life you must use this tool.", meaning_of_life)

model = Model("gpt-3.5-turbo", 0, os.environ["OPENAI_API_KEY"])
agent = Agent(model, [meaning_of_life_tool])


class TestAgent(unittest.TestCase):
    def test_meaning_of_life(self):
        global meaning_of_life_run_count
        old_count = meaning_of_life_run_count
        response = agent("What is the meaning of life? Give the answer without text; just the numerical answer.")
        self.assertEqual("2138384", response)
        self.assertEqual(meaning_of_life_run_count, old_count + 1)

        # example asserts:
        # self.assertTrue("FOO".isupper())
        # self.assertFalse("Foo".isupper())
        # s = "hello world"
        # self.assertEqual(s.split(), ["hello", "world"])
        # # check that s.split fails when the separator is not a string
        # with self.assertRaises(TypeError):
        #     s.split(2)


if __name__ == "__main__":
    unittest.main()
