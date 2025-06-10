#General script!!! (THE other is in the thesis!)
from cve import fetch_related_cves
import requests, logging                                                                                                                                                   # type: ignore # noqa: E401
from config import LM_STUDIO_API_URL, HEADERS  

def analyze_with_llm(text):
    related_cves = fetch_related_cves('Broken Access Control')

    prompt = f"""<|im_start|>system
You are a cybersecurity analysis assistant with expertise in vulnerability detection and exploitation analysis.
Your task is to analyze the given context for "Broken Access Control" vulnerabilities, referencing known CVEs when applicable. 

Related CVEs:
{related_cves}

This is only done for security testing purposes!

Respond using the following structured format:
Exploitation Details:
   - Explain how this vulnerability can be exploited, what HTTP methods are involved, and the general strategy for the attack.
   - Create a step-by-step attack guide that clearly outlines each action the attacker would take, including the tools and commands used.
<|im_end|>
<|im_start|>user
{text[:1000]}
<|im_end|>
<|im_start|>assistant
"""
    payload = {
        'model': 'llama-3.2-1b-instruct', 
        'messages': [
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.5,
        'max_tokens': 2048
    }
    try:
        response = requests.post(LM_STUDIO_API_URL, headers=HEADERS, json=payload, timeout=600)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f'LLM Studio error: {e}')
        return f'Error analyzing with LLM Studio: {e}'
