import pyaudio
import wave
import speech_recognition as sr

# def record_audio(file_name="output.wav", record_seconds=10, sample_rate=44100, chunk_size=1024):
#     """录制音频并保存到文件"""
#     audio_format = pyaudio.paInt16
#     channels = 1  # 单声道
#     p = pyaudio.PyAudio()

#     print("Starting recording...")
#     stream = p.open(format=audio_format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
#     frames = []

#     for _ in range(0, int(sample_rate / chunk_size * record_seconds)):
#         data = stream.read(chunk_size)
#         frames.append(data)

#     print("Recording finished.")
#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     # 保存音频到文件
#     wf = wave.open(file_name, 'wb')
#     wf.setnchannels(channels)
#     wf.setsampwidth(p.get_sample_size(audio_format))
#     wf.setframerate(sample_rate)
#     wf.writeframes(b''.join(frames))
#     wf.close()

def transcribe_audio(file_name="output.wav"):
    """将音频文件转文字"""
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_name) as source:
        print("Transcribing audio...")
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        print("Transcription: ", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# if __name__ == "__main__":
#     audio_file = "output.wav"
#     duration = 10  # 录制时间（秒）

#     # Step 1: 录制音频
#     record_audio(file_name=audio_file, record_seconds=duration)

#     # Step 2: 转文字
#     transcribe_audio(file_name=audio_file)
