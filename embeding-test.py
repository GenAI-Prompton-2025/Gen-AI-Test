import os
import re
import pandas as pd
import numpy as np
import tiktoken
import openai
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

df_wiki_data=pd.read_csv(os.path.join(os.getcwd(),'data/categorized_output_filtered.csv'))
# print("content: ", df_wiki_data['content'])


pd.options.mode.chained_assignment = None #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#evaluation-order-matters

# s is input text
def normalize_text(s, sep_token = " \n "):
    s = re.sub(r'\s+',  ' ', s).strip()
    s = re.sub(r". ,","",s)
    # remove all instances of multiple spaces
    s = s.replace("..",".")
    s = s.replace(". .",".")
    s = s.replace("\n", "")
    s = s.strip()
    
    return s

df_wiki_data['content']= df_wiki_data["content"].apply(lambda x : normalize_text(x))

tokenizer = tiktoken.get_encoding("cl100k_base")
df_wiki_data['n_tokens'] = df_wiki_data["content"].apply(lambda x: len(tokenizer.encode(x)))
df_wiki_data = df_wiki_data[df_wiki_data.n_tokens<8192]
# len(df_wiki_data)
# print(df_wiki_data)

sample_encode = tokenizer.encode(df_wiki_data.content[0]) 
decode = tokenizer.decode_tokens_bytes(sample_encode)
# print(decode)

print(openai)

def generate_embeddings(content, model=deployment_embedding_name):
    return client.embeddings.create(input = [content], model=model).data[0].embedding

# model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
df_wiki_data['content_vector'] = df_wiki_data["content"].apply(lambda x : generate_embeddings (x, model = deployment_embedding_name)) 
print(df_wiki_data)
