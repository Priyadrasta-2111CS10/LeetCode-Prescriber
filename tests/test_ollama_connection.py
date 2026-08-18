import requests


url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3.2:latest",
    "prompt": "Return a JSON object with a hello message.",
    "stream": False,
    "format": "json",
}

try:

    response = requests.post(
        url,
        json=payload,
        timeout=120,
    )

    print("Status:", response.status_code)

    print("Response:")
    print(response.text)

except requests.RequestException as exc:

    print("Connection failed:")
    print(exc)