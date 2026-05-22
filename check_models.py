from google import genai

client = genai.Client(api_key="AIzaSyDhtpMM-QWu1DkzA85OZpxRUTjzbwHOSHo")

print("Available models:")
print("=" * 50)

try:
    models = client.models.list()
    for model in models:
        print(f"Model: {model.name}")
except Exception as e:
    print(f"Error: {e}")
