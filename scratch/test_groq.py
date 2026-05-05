import os
from groq import Groq

try:
    client = Groq(api_key=None)
    print("Cliente Groq criado com None")
except Exception as e:
    print(f"Erro ao criar cliente Groq com None: {e}")

try:
    client = Groq(api_key="")
    print("Cliente Groq criado com string vazia")
except Exception as e:
    print(f"Erro ao criar cliente Groq com string vazia: {e}")
