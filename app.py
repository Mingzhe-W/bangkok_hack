from flask import Flask, request, jsonify
import os

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# 创建保存音频文件的目录
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

    # 模拟 AI 响应
    response = {"message": f"i hear you, i will sendt the request {file_path}"}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
