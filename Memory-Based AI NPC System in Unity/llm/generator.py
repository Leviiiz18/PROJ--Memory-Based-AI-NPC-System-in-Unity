import requests

OPENROUTER_API_KEY = ""
MODEL = "mistralai/mixtral-8x7b-instruct"

def generate_llm_response(prompt):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Unity NPC AI System"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("LLM ERROR:", response.text)
        return "The NPC stares silently."

    result = response.json()

    try:
        return result["choices"][0]["message"]["content"]
    except:
        print("Unexpected response:", result)

        return "The NPC seems confused."
