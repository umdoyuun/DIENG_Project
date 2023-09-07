# 1. 개발배경 및 목적

강의나 회의에서 중요한 내용을 기억하는 것은 매우 중요합니다. 하지만 강의 또는 회의를 진행할 때 오랜 시간 동안 집중력을 유지하기는 어렵습니다. 이러한 문제를 해결하기 위해 프로젝트를 기획하였습니다. 이 프로젝트의 목적은 실시간으로 음성 녹음을 하고 음성 인식 및 요약하여 중요한 내용을 추출하고 디스코드 봇을 통해 구독자들에게 실시간 알림을 전송하는 것입니다. 또한 다양한 언어를 사용하는 참가자를 위한 번역 기능이 있습니다.

# 2. 개발환경 및 개발언어

● 개발 언어: Python
● 데이터베이스: SQLite
● 웹 애플리케이션: Flask
● 하드웨어: 라즈베리파이


# 3. 시스템 구성 및 아키텍처
스템 구성 및 아키텍처
### I.시스템 개요
● 이 프로젝트는 Discord를 통해 사용자에게 텍스트 요약 서비스를 제공하는 시스템입니다. Discord 봇과 웹 인터페이스를 통해 사용자의 텍스트를 받아, 요약된 텍스트를 반환합니다.

### II. 구성 요소
● Discord 봇 (DIscordBot.py)
사용자 인터페이스 역할을 하며, 텍스트 요약을 위한 텍스트를 수집합니다.
Discord API와 통신하여 사용자 입력을 받고 출력을 제공합니다.

● Text Summarizer (summarize.py)
WAV파일을 음성 인식하여 텍스트를 추출하고 요약하는 알고리즘을 구현한 부분입니다.
speech_recognition라이브러리와 Google Web Speech API를 통해 음성을 인식합니다.
네이버 CLOVA Summary API를 통해 텍스트를 요약합니다.
봇으로부터 전달받은 텍스트를 요약하고 결과를 반환합니다.

● Database (dic_sumbot.db)
사용자 데이터와 요약 결과를 저장합니다.
SQLite 데이터베이스를 사용하여 데이터를 관리합니다.

● Web Interface (static, templates)
웹 애플리케이션의 정적 파일과 HTML 템플릿을 관리합니다.
Flask 웹 프레임워크를 사용합니다.

● 하드웨어(rasberryPi/main.py, rasberryPi/record.py)
Flask를 통해 서버와 통신합니다.
start 요청 시 record.py를 호출 해 실시간 WAV파일을 녹음 해 서버로 전송합니다.
stop 요청 시 녹음 중이던 WAV파일을 서버로 전송 후 녹음을 중지합니다.


### III. 데이터 흐름도

### IV. 기술 스택
● Programming Language: Python
● Database: SQLite
● Web Framework: Flask
● API: Discord API, 네이버 클로바 요약 API

### V. 보안
● 데이터베이스에 사용자 데이터와 요약 결과를 암호화하여 저장합니다.
● Discord 봇과 데이터베이스 사이의 통신은 암호화된 채널을 통해 이루어집니다.

### VI. 배포
● Discord 봇은 Discord 서버에 호스팅됩니다.
● 웹 인터페이스는 별도의 웹 서버에 배포될 수 있습니다.

### VII. 스케일링
● 데이터베이스는 필요에 따라 클러스터링이나 샤딩을 통해 확장할 수 있습니다.
● 텍스트 요약 알고리즘은 병렬 처리를 통해 더 빠른 응답 시간을 제공할 수 있습니다.


# 4. 프로젝트 주요기능

### I. Discord 봇
● 목적: Discord 봇은 사용자와 시스템 간의 주요 인터페이스입니다. 사용자로부터 텍스트를 받아 요약 및 번역하고, 결과를 반환합니다.

● 기능: 
■ 사용자 명령어 인식: 특정 명령어나 키워드를 통해 사용자의 의도를 파악합니다.
■ 텍스트 수집: 사용자로부터 제공된 텍스트를 수집하여 요약 및 번역 작업을 위해 준비합니다.
■ 요약 결과 전달: 요약 및 번역 알고리즘이 적용된 텍스트를 사용자에게 반환합니다.
■ 사용 기술: Python, Discord API

### II. 음성 인식
● 목적: 녹음된 WAV 파일로부터 음성을 인식하여 텍스트를 추출합니다.

● 기능: 
■ 텍스트 수집: 사용자 혹은 라즈베리파이로부터 제공받은 WAV 파일을 수집합니다.
■ 음성 인식 알고리즘 적용: WAV 파일로부터 텍스트를 추출합니다.
■ 사용 기술: Python, speech_recogntion 라이브러리, Google Web Speech API

### III. 텍스트 요약
● 목적: 대량의 텍스트 정보를 짧고 간결한 형태로 요약하여 사용자에게 효율적인 정보 전달을 도와줍니다.

● 기능: 
■ 자연어 처리: 제공된 텍스트를 분석하여 주요 내용을 파악합니다.
■ 요약 알고리즘 적용: 주요 내용을 기반으로 텍스트를 요약합니다.
■ 사용 기술: Python, 네이버 클로바 요약 API

### IV. 텍스트 번역
● 목적: 다양한 언어의 사용자를 고려하여 

● 기능: 
■ 텍스트 수집: 제공된 정보를 바탕으로 데이터베이스에서 필요한 텍스트를 가져옵니다.
■ 번역 알고리즘 적용: 요청된 언어로 텍스트를 번역합니다.
■ 사용 기술: Python, googletrans 라이브러리

### V.  데이터베이스 관리
● 목적: 사용자 데이터와 텍스트 요약 결과를 안전하게 저장하고 관리합니다.
● 기능: 
■ 데이터 저장: 요약된 텍스트와 관련 데이터를 데이터베이스에 저장합니다.
■ 데이터 조회: 필요에 따라 저장된 데이터를 조회할 수 있습니다.
■ 데이터 업데이트: 새로운 정보가 있을 경우 데이터베이스를 업데이트합니다.
■ 사용 기술: SQLite, Python

### VI. 프로그램 소개
● 회원가입 및 로그인
■ 회원가입 시 회원 정보를 데이터 베이스에 저장합니다.
■ 데이터베이스에서 회원 정보를 통해 로그인 합니다.
● 토큰 입력
■ 디스코드 디벨로퍼 포털(https://discord.com/developers/docs/intro)에서 생성한 봇의 토큰을 입력합니다.
● 요약봇 제어
■ 1. 봇 실행 및 종료: 실행 버튼 클릭 시 봇이 실행되며 실행 메시지를 보냅니다. 종료 버튼 클릭 시 봇이 종료 됩니다.


■ 2. 라즈베리파이 녹음: 재생 버튼 클릭 시 라즈베리파이의 Record.py가 실행되며 3분에 한 번씩 WAV파일을 보내어 요약 메시지를 출력합니다. 중지 버튼 클릭 시 마지막에 녹음 중이던 WAV파일을 보내고 요약 메시지를 출력합니다.
■ 3-4. 오디오 파일 업로드: 요약하고 싶은 오디오 파일을 올리고 요약된 내용을 메시지로 전송합니다.

● 디스코드 명령어
■ 원하는 날짜의 요약본을 요청한 경우 해당 날짜의 요약본을 메시지로 출력합니다.
■ 원하는 날짜의 요약본을 번역하여 요청한 경우 날짜의 요약본을 번역하여 출력합니다. 영어, 일본어, 중국어의 번역을 지원합니다.


# 5. 기대효과 및 활용분야

I. 기대 효과
● 정보 효율성 증대: 텍스트를 빠르고 정확하게 요약함으로써 사용자가 정보를 더 효율적으로 소비할 수 있습니다.
● 시간 절약: 큰 양의 텍스트를 읽고 이해하는 데에 걸리는 시간을 줄여, 사용자에게 시간을 절약해 줍니다.
● 사용자 경험 향상: Discord를 통해 간편하게 텍스트 요약 서비스를 이용할 수 있어 사용자 경험이 향상됩니다.
● 데이터 관리: 사용자 데이터와 요약 결과를 안전하게 저장하여, 재사용이나 분석에 활용할 수 있습니다.
II. 활용 분야
● 교육: 학생들이 빠르게 많은 양의 정보를 습득할 수 있도록 도와줍니다.
● 연구 및 분석: 대량의 텍스트 데이터를 빠르게 분석하고 핵심 내용을 추출하는 데 활용할 수 있습니다.
● 뉴스 및 미디어: 다양한 뉴스 기사나 보고서를 빠르게 요약하여, 사용자에게 제공할 수 있습니다.
● 커뮤니케이션 플랫폼: Discord 뿐만 아니라 다른 메신저 또는 커뮤니케이션 플랫폼에서도 활용 가능합니다.
● 기업용 애플리케이션: 회의록, 보고서, 이메일 등을 요약하여 업무 효율성을 높일 수 있습니다.

# 6 기타(프로젝트 추가 설명 등 자료 첨부 가능)
### I.사용 API, 라이브러리 설명
### ● 네이버 CLOVA Summary API(텍스트 요약)
■ 텍스트를 효과적으로 간결하게 요약하는 데 사용되는 API입니다. 주로 뉴스 기사, 논문, 문서 등에서 긴 텍스트에서 정보를 추출하는 데 활용됩니다.
■ 영어로 번역하여 요약하고 다시 한글로 번역하는 다른 요약 알고리즘과 달리 한글로 문장의 중요도를 고려하여 요약 합니다.
■ 2000자 이내의 텍스트를 요약하는 것을 지원하고, 사용하기 위해 네이버 개발자 포털에서 API 키를 지급 받아야 합니다.

### ● speech_recognition 라이브러리(음성 인식)
■ 여러 음성 인식 엔진을 지원하는 라이브러리입니다. 대표적으로 Google Web Speech API, IMB Waston, Microsft Bing Voice Recognition 등의 엔진이 있고, 본 프로젝트에서는 Google Web Speech API를 사용해 음성 인식을 진행하였습니다.
■ 다양한 언어를 지원하므로 다국어 음성 데이터도 처리 가능합니다.
■ 오디오 파일을 읽고 처리하여 음성을 텍스트로 변환할 수 있습니다.

### ● googletrans 라이브러리(번역)
■ Google 번역 엔진을 기반으로 다양한 언어의 문서, 대량의 문서를 번역할 수 있는 강력한 번역 서비스를 제공합니다.
■ 언어 감지를 제공하여, 어떤 언어로 작성된 텍스트인지 자동으로 감지하여 번역을 설정할 수 있습니다.
■ 본 프로젝트에서는 한국어를 영어, 중국어, 일본어로 번역하는 기능을 수행하였습니다.
