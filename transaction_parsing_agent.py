import re
import requests

# 定义 Hyperbolic API 配置
HYPERBOLIC_API_URL = "https://api.hyperbolic.xyz/v1/completions" 
HYPERBOLIC_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtendhbmcxMDMwQG91dGxvb2suY29tIiwiaWF0IjoxNzMxNzAxODIyfQ.wS7uENmYmYlBdVNVmo9C4eQfWrP5nFWq8JjM7Ii16lc"

# def extract_ens_address(sentence):
#     """
#     extract ENS addresses from the sentence
#     """
#     # regex pattern to match ENS addresses
#     pattern = r"\b[a-zA-Z0-9\-]+\.eth\b"
#     return re.findall(pattern, sentence)

def parse_transfer_with_hyperbolic(sentence):
    """
    Use Hyperbolic API to parse English transfer statements
    """
    
    # # extract ENS addresses
    # ens_addresses = extract_ens_address(sentence)
    # sender = ens_addresses[0] if len(ens_addresses) > 0 else None
    # receiver = ens_addresses[1] if len(ens_addresses) > 1 else None
    
    # if not sender and not receiver:
    #     return {"error": "No ENS address found in the sentence"}
    # 定义 Prompt
    prompt = f"""
    Extract transfer details from the following sentence:
    Sentence: "{sentence}"
    Output as JSON with the keys: from, to, amount, unit, chain_name. and nothing else.
    If information is missing, use null. Ensure ENS addresses (.eth) are correctly identified.

    """

    
    payload = {
        "prompt": prompt,
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "max_tokens": 150,
        "temperature": 0.0,
        "top_p": 1.0
    }
    
    headers = {
        "Authorization": f"Bearer {HYPERBOLIC_API_KEY}",
        "Content-Type": "application/json"
    }

   
    response = requests.post(HYPERBOLIC_API_URL, json=payload, headers=headers)

    
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        return {"error": f"API call failed with status code {response.status_code}: {response.text}"}

# exapmple testing
examples = [
    "alice.eth sent 10 ETH to bob.eth on Base",
    "Please transfer 5 Bitcoin to charlie.eth on btc",
    "Can you send 100 USDT to david.eth on Ethereum?",
    "I want to transfer 0.5 DOGE to frank.eth on Polygon",
    "This sentence does not contain any ENS address"
]

# testing
for sentence in examples:
    result = parse_transfer_with_hyperbolic(sentence)
    print(f"Input: {sentence}")
    print(f"Output: {result}\n")
