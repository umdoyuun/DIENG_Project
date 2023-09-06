import pyaudio
import wave
import signal
import sys
import requests

TOKEN = sys.argv

# 오디오 데이터를 WAV 파일로 저장하는 함수
def save_audio_data(frames):
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

# 오디오 데이터 전송 함수
def send_audio():
    url = 'http://172.16.37.104:5000/upload_audio'
    with open('audio.wav', 'rb') as f:
        files={'audio': f}
        data={'token' : TOKEN}
        response=requests.post(url, files=files, data=data)
    print(response.text)

# SIGINT 시그널 핸들러 
def signal_handler(sig, frame):
    print('녹음 중단')
    save_audio_data(frames)
    send_audio()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 44100  
CHUNK = 1024  
RECORD_SECONDS = 180
OUTPUT_FILENAME = "audio.wav"  

audio = pyaudio.PyAudio()

while True:
    
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("녹음 시작")

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    
   
    # 녹음 완료 후 저장 및 전송 작업 수행   
    save_audio_data(frames)  
    send_audio()

    print("녹음 완료 및 전송 완료")

    # 스트림 종료 
    stream.stop_stream()
    stream.close()

# PyAudio 종료   
audio.terminate()