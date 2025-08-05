# Big OMG API

Big OMG is a Flask-based API that analyzes the time complexity of user-inputted code. It demonstrates how to use configurable AI models (or defaults to Claude 4 Opus) to provide detailed time complexity analysis and explanations, helping developers optimize their algorithms.

## Features

- **Time Complexity Analysis**: Automatically determines Big O notation for code snippets
- **Detailed Explanations**: Provides step-by-step reasoning for the complexity analysis
- **Multiple AI Models**: Supports different AI models for analysis using litellm
- **RESTful API**: Simple HTTP endpoints for easy integration

## API Usage

### Endpoint: `POST /api/get-big-o`

Analyzes the time complexity of provided code.

#### Request Body

```json
{
  "code": "your code snippet here",
  "model": "your model name here" // optional, defaults to claude-4-20250514
}
```
all supported models: https://models.litellm.ai/

#### Example Request

```bash
curl -X POST http://localhost:5000/api/get-big-o \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def addTwoNumbers(l1, l2):\n    dummy = ListNode(0)\n    current = dummy\n    carry = 0\n    \n    while l1 or l2 or carry:\n        x = l1.val if l1 else 0\n        y = l2.val if l2 else 0\n        \n        total = x + y + carry\n        carry = total // 10\n        \n        current.next = ListNode(total % 10)\n        current = current.next\n        \n        if l1: l1 = l1.next\n        if l2: l2 = l2.next\n    \n    return dummy.next",
    "model": "anthropic/claude-3-opus"
  }'
```

#### Response

```json
{
  "big_o": "O(max(m, n))",
  "explanation": "Time Complexity: O(max(m, n)) Where m is the length of linked list l1 and n is the length of linked list l2...",
  "model": "claude-opus-4-20250514"
}
```

## How It Works

### 1. Code Analysis Process

The API uses a system prompt and a user prompt and then passes that into liteLLM's `completion` function which handles LLM-specific formatting so the code does not have to be different for different LLMs:

```python
# The AI service prompts the model with a specific format
mgs = [
    {
        "role": "system",
        "content": "You are an AI assistant that helps users analyze the time complexity of code snippets. Always start your response with the main time complexity in the format 'Time Complexity: O(...)' followed by your detailed explanation."
    },
    {
        "role": "user",
        "content": f"I have the following piece of code:\n\n{code}\n\nWhat is the time complexity of this code and explain your reasoning?"
    }
]
response = completion(
            model=llm, # passed in from the request
            messages=mgs,
            temperature=1
        )
```

### 2. Response Extraction

The API uses regex patterns to extract the time complexity from the AI response:

```python
# First try to find the main time complexity at the beginning
main_complexity_pattern = r'Time Complexity:\s*O\([^)]+\)'
main_match = re.search(main_complexity_pattern, explanation, re.IGNORECASE)

if main_match:
    time_complexity = main_match.group(0).split(':')[1].strip()
else:
    # Fallback to finding any Big O notation, preferring more complex ones
    big_o_pattern = r'O\([^)]+\)'
    matches = re.findall(big_o_pattern, explanation)
    if matches:
        time_complexity = max(matches, key=len)
```

### 3. Error Handling

The API includes comprehensive error handling:

```python
@app.post('/api/get-big-o')
def get_big_o():
    req = request.get_json()
    if 'code' not in req:
        return Response("Missing required parameter 'code'", status=422)
    # ... rest of the logic
```

## Setup and Installation

### Prerequisites

- Python 3.12
- pip

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/big-omg-api.git
cd big-omg-api
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
# Create a .env file with your API keys
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

5. Run the application:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Project Structure

```
big-omg-api/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── app.yaml              # Google App Engine configuration
├── src/
│   └── services/
│       └── ai.py         # AI service for code analysis
└── README.md
```

## Frontend Integration

This is the backend API only. The frontend React application is located at: https://github.com/Qlwentt/big-omg-react

Live demo: https://big-omg-react.uw.r.appspot.com/

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
