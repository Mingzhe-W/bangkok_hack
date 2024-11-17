# Voice Is All You Need
This project is built for ETH Global Bangkok



Our project is an AI agent that enables voice-based blockchain transactions. Simply interact with the agent using your voice to complete secure on-chain transfers. The process is smooth yet highly secure thanks to voiceprint signatures and on-chain key voice recording snippets. To protect sensitive info and prevent direct exposure of voiceprints, users can make limited edits (e.g., masking or tuning) to the voice before it’s recorded on-chain. We also use ZKPs to provide proof of editing. 



Our project leverages several key technologies to bring voice-based blockchain transactions to life:
1. AI Agent: Built with the Hyperbolic Inference API, our agent analyzes conversational context to extract transaction-related details efficiently.
2. Blockchain Integration: Transactions are executed on Ethereum and L2 chains using their SDKs and APIs, ensuring fast and reliable on-chain interactions.
3. Voiceprint Signatures: A GMM model trains user-specific voiceprint recognition, verifying the speaker matches the wallet owner. The inference process is secured using ZKML(EZKL) to prevent inference result from being tempered.
4. Proof of Editing: We custom-designed zero-knowledge circuits using Plonky2 to validate limited edits (masking or tuning) on voice data. This ensures sensitive information remains private while proving the integrity of edits.
5. ENS Service: ENS is integrated to resolve wallet addresses, improving user experience by avoiding cumbersome verbal address exchanges. 
6. Onchain Data Storage: Large audio data and ZKPs are stored and accessed via decentralized storage solutions like Filecoin's Storacha, ensuring scalability and performance.



You can try our project by 

Frontend: at root dir

```shell
python -m http.server

```

Beckend: at beckend folder

```shell
python app.py
```

and open a browser to enter

```shell
http://localhost:8000
```



Main files explains:



beckend/app.py: 						beckend main program

beckend/voice_print.py: 				   voice print (not integrated into main program yet)

beckend/hyperbolic_parsing_agent.py: 	LLM based speech analysis using hyperbolic API

beckend/audio_transcriptor.py: 		    speech to text

index.html: 							frontend

zero_knowledge_proof/src/main.rs: 	     zk circuits for Proof of Editing 





 
