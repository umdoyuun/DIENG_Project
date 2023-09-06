import speech_recognition as sr
import requests
import json
from datetime import datetime  # 날짜와 시간 처리 라이브러리

def summarize_audio(path):
    r = sr.Recognizer()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = ""
    #audio_path = 'received_audio.wav'
    #네이버 클로바 요약봇 api header
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "jh19pjvtf0",
        "X-NCP-APIGW-API-KEY": "HeVGwkTQohOuVxBEFxJjpFxO4X6LbQOiFFcH8OU2",
        "Content-Type": "application/json"
    }

    with sr.AudioFile(path) as source:
        audio = r.record(source)

    try:
        t = r.recognize_google(audio, language='ko-KR')
    except (sr.UnknownValueError, sr.RequestError) as e:
        print("Google Speech Recognition service error: " + str(e))
        t = ""

    print("원본 텍스트:\n", t)
    texts = [t[i:i+2000] for i in range(0, len(t), 2000)]

    for i, text in enumerate(texts):
        if len(text) >= 1200:
            cnt = 3
        elif len(text) >= 500:
            cnt = 2
        else:
            cnt = 1
        body = {
            "document": {
                "content": text
            },
            "option": {
                "language": "ko",
                "model" : "general",
                "tone" : 2,
                "summaryCount" : cnt
            }
        }

        try:
            response = requests.post("https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize", headers=headers, data=json.dumps(body))
            response.raise_for_status()
            summary = response.json()["summary"]

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(response.text)
        except KeyError:
            print("Key 'summary' not found in the API response.")
        except json.JSONDecodeError:
            print("An error occurred while parsing the API response.")
        else:
            result += current_date + ' 요약된 텍스트 ' + str(i+1) + ':\n' + summary+'\n'
            print("요약된 텍스트 %d:\n" % (i + 1), summary)
        return result