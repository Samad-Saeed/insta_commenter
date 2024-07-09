import requests

def get_gpt_response(prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        return response_json['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == "__main__":
    api_key = ""
    prompt = "write me a nice comments."
    answer = get_gpt_response(prompt, api_key)
    print(answer)
