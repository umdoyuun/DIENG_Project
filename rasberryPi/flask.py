import requests

url = 'http://172.30.1.49:5000/upload'  # 노트북의 IP 주소와 포트 설정
files = {'audio': open('audio.wav', 'rb')}  # 보낼 오디오 파일 경로 설정

response = requests.post(url, files=files)

print(response.text)