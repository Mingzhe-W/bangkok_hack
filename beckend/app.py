from flask import Flask, request, jsonify
import os

from flask_cors import CORS

from audio_transcriptor import transcribe_audio
from hyperbolic_parsing_agent import parse_transfer_with_hyperbolic

import time
import os

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

i = 0

@app.route('/api/audio', methods=['POST'])
def audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(file_path)

    # speech to text
    text = transcribe_audio(file_path)
    print(text)

    global i
    response = parse_transfer_with_hyperbolic(text)
    if response.get("error"):
        response = {"message": f"there is something wrong with the agent API"}
        return jsonify(response), 200
    
    else:
        
        if (not response.get("to")) or (not response.get("amount")) or (not response.get("unit")):
            {"message": f"I don't understand, can you repeat?"}
            return jsonify(response), 200
        else:
            if i == 0:
                response = {"message": f"Sending {response['amount']} {response['unit']} to {response['to']}. Confirm to proceed?"}
                i = 1
                return jsonify(response), 200
            else:
                os.system("npx hardhat run sendTx.js --network sepolia")
                response = {"message": f"Done! The transaction has been sent."}
                i = 0
                return jsonify(response), 200

            
    








if __name__ == '__main__':
    app.run(debug=True, port=5000)
