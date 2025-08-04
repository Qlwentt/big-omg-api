import re
from litellm import completion



class AI:
    def get_big_o(self, code, llm):
        mgs = [
            {"role": "system", "content": "You are an AI assistant that helps users analyze the time complexity of code snippets. Always start your response with the main time complexity in the format 'Time Complexity: O(...)' followed by your detailed explanation."},
            {"role": "user", "content": f"I have the following piece of code:\n\n{code}\n\nWhat is the time complexity of this code and explain your reasoning?"},
        ]
        response = completion(
            model=llm,
            messages=mgs,
            temperature=1
        )

        explanation = response.choices[0].message.content.strip()
        
        # First try to find the main time complexity at the beginning
        main_complexity_pattern = r'Time Complexity:\s*O\([^)]+\)'
        main_match = re.search(main_complexity_pattern, explanation, re.IGNORECASE)
        
        if main_match:
            time_complexity = main_match.group(0).split(':')[1].strip()
        else:
            # Fallback to finding any Big O notation, but prefer more complex ones
            big_o_pattern = r'O\([^)]+\)'
            matches = re.findall(big_o_pattern, explanation)
            
            if matches:
                # Prefer the most complex notation (longer strings usually indicate more complex complexity)
                time_complexity = max(matches, key=len)
            else:
                time_complexity = "Unknown"

        return {"big_o": time_complexity, "explanation": explanation, "model": llm}