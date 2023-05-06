import openai
import os
import re


openai.api_key = os.environ.get("OPENAI_API_KEY")

class OpenAI:
    def get_big_o(self, code):
        messages = [
            {"role": "system", "content": "You are an AI assistant that helps users analyze the time complexity of code snippets."},
            {"role": "user", "content": f"I have the following piece of code:\n\n{code}\n\nWhat is the time complexity of this code and explain your reasoning?"},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
        )

        explanation = response['choices'][0]['message']['content'].strip()
        big_o_pattern = r'O\([a-zA-Z0-9\+\-\*/^ ]+\)'
        match = re.search(big_o_pattern, explanation)
        time_complexity = match.group(0) if match else "Unknown"

        return {"big_o": time_complexity, "explanation": explanation}