import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

client = AzureOpenAI(    
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key        = os.getenv("AZURE_OPENAI_API_KEY"),
    api_version    = os.getenv("OPENAI_API_VERSION")
)

deployment_name = os.getenv("DEPLOYMENT_NAME")
deployment_embedding_name = os.getenv("DEPLOYMENT_EMBEDDING_NAME")

# Create your first prompt
system_message = """너는 긍정과 부정을 구분할 수 있는 에이전트야. 결과는 JSON 형식으로 공백 없이 반환해줘. 답변 예:{"1": "긍정", "2": "부정"}"""
user_message = """1. 모니터가 너무 뜨거워. 2. 모니터가 시장 반응이 너무 뜨거워."""

# Simple API Call
response = client.chat.completions.create(
    model=deployment_name,
    max_tokens=60,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
)

print(response.choices[0].message.content)