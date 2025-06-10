import google.generativeai as genai

genai.configure(api_key="your api key")

for m in genai.list_models():
    print(m.name)
