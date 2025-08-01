import re
from litellm import completion



class AI:
    def get_big_o(self, code, llm):
        mgs = [
            {"role": "system", "content": "You are an AI assistant that helps users analyze the time complexity of code snippets."},
            {"role": "user", "content": f"I have the following piece of code:\n\n{code}\n\nWhat is the time complexity of this code and explain your reasoning?"},
        ]
        response = completion(
            model=llm,
            messages=mgs,
            temperature=1
        )

        explanation = response.choices[0].message.content.strip()
        big_o_pattern = r'O\([a-zA-Z0-9\+\-\*/^ ]+\)'
        match = re.search(big_o_pattern, explanation)
        time_complexity = match.group(0) if match else "Unknown"

        return {"big_o": time_complexity, "explanation": explanation, "model": llm}