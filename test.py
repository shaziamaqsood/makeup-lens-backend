import requests

url = "http://127.0.0.1:8000/analyze"

files = {"file": open("test.jpeg", "rb")}

res = requests.post(url, files=files)

print(res.text)