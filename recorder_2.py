import pyaudio
import wave
import tkinter as tk
from tkinter import messagebox
import threading

class AudioRecorder:
    def __init__(self, file_name="output.wav", sample_rate=44100, chunk_size=1024, channels=1):
        self.file_name = file_name
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.audio_format = pyaudio.paInt16
        self.frames = []
        self.is_recording = False
        self.thread = None

    def start_recording(self):
        """开始录音"""
        self.is_recording = True
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        print("Recording started.")
        
        while self.is_recording:
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)

    def stop_recording(self):
        """停止录音"""
        if self.is_recording:
            self.is_recording = False
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()

            # 保存音频
            wf = wave.open(self.file_name, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.audio_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            print(f"Recording stopped. File saved as {self.file_name}")

class RecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")
        self.recorder = AudioRecorder()
        self.is_recording = False

        # 创建按钮
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording, bg="green", fg="white", font=("Arial", 12))
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, bg="red", fg="white", font=("Arial", 12))
        self.stop_button.pack(pady=20)
        self.stop_button["state"] = "disabled"  # 初始状态禁用

    def start_recording(self):
        """点击开始录音"""
        if not self.is_recording:
            self.is_recording = True
            self.start_button["state"] = "disabled"
            self.stop_button["state"] = "normal"

            # 在后台线程中运行录音
            self.recorder.thread = threading.Thread(target=self.recorder.start_recording)
            self.recorder.thread.start()

            messagebox.showinfo("Recording", "Recording has started. Click 'Stop Recording' to finish.")

    def stop_recording(self):
        """点击停止录音"""
        if self.is_recording:
            self.is_recording = False
            self.start_button["state"] = "normal"
            self.stop_button["state"] = "disabled"

            # 停止录音
            self.recorder.stop_recording()

            messagebox.showinfo("Recording", f"Recording stopped. File saved as {self.recorder.file_name}")

# 创建主窗口并运行应用
if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderApp(root)
    root.mainloop()
