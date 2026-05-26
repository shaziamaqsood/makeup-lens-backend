from google import genai

client = genai.Client(api_key="AIzaSyDMHOrPaMXph5nrwBmmlXOkA0f-_lvBvus")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="hello"
)

print(response.text)