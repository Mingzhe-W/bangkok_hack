from flask import Flask, request, jsonify
import os

from flask_cors import CORS

from audio_transcriptor import transcribe_audio

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/audio', methods=['POST'])
def audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(file_path)

    # 转录音频
    text = transcribe_audio(file_path)
    print(text)

    # 模拟 AI 响应
    response = {"message": f"i hear you, i will sendt the request and order a mango sticky rice for you"}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
