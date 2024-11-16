# traditional nlp solution to parse transfer sentences
import spacy

# load the spaCy model
nlp = spacy.load("en_core_web_sm")

# supported units and blockchains
SUPPORTED_UNITS = {
    "eth": "ETH",
    "ethereum": "ETH",
    "btc": "BTC",
    "bitcoin": "BTC",
    "usdt": "USDT",
    "tether": "USDT",
    "doge": "DOGE",
    "dogecoin": "DOGE",
    "ltc": "LTC",
    "litecoin": "LTC",
    "bnb": "BNB",
    "binance coin": "BNB",
    "ada": "ADA",
    "cardano": "ADA",
    "xrp": "XRP",
    "ripple": "XRP"
}

# define supported blockchains
SUPPORTED_CHAINS = {
    "ethereum": "Ethereum",
    "binance smart chain": "Binance Smart Chain",
    "bsc": "Binance Smart Chain",
    "polygon": "Polygon",
    "matic": "Polygon",
    "solana": "Solana",
    "tron": "Tron",
    "avalanche": "Avalanche"
}

def parse_transfer(sentence):
    """
    使用 NLP 解析英文转账语句，并支持更多单位和区块链名称
    """
    
    doc = nlp(sentence)
    
    sender = None
    receiver = None
    amount = None
    unit = None
    chain_name = None
    
    
    for token in doc:
       
        if token.dep_ == "nsubj" and sender is None:  
            sender = token.text
        elif token.dep_ == "pobj":  
            receiver = token.text
        
 
        if token.like_num: 
            amount = float(token.text)
        
  
        if token.text.lower() in SUPPORTED_UNITS:
            unit = SUPPORTED_UNITS[token.text.lower()]
        
 
        if token.text.lower() in SUPPORTED_CHAINS:
            chain_name = SUPPORTED_CHAINS[token.text.lower()]
  
    if not sender or not receiver or not amount or not unit:
        return {"error": "Unable to parse the sentence"}
    
    
    return {
        "from": sender,
        "to": receiver,
        "amount": amount,
        "unit": unit,
        "chain_name": chain_name or "Unknown"
    }

