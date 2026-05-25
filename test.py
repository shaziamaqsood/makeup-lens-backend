from google import genai

client = genai.Client(api_key="AIzaSyBZgkwHWjdJ2al2CjRGyKjlEc4B2RVxc4w")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="hello"
)

print(response.text)