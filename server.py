from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import speech_recognition as sr
import requests
import json
import sqlite3
import datetime
from summarize import summarize_audio
from werkzeug.utils import secure_filename
import subprocess
import os
import atexit


app = Flask(__name__)
app.secret_key = "01234_key"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

subprocesses = {}

# 데이터 베이스 생성
def create_table():
    connection = sqlite3.connect('dic_sumbot.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (token TEXT, username TEXT, password TEXT, date TEXT, summarize TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS sum_message (token TEXT, summarize TEXT)')
    connection.commit()
    connection.close()

#서버 종료시 모든 서브 프로세스 종료
def cleanup_subprocesses():
    for token, process in subprocesses.items():
        process.terminate()

# Existing routes
@app.route('/')
def index():
    return render_template('index.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('dic_sumbot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if cursor.fetchone():
            session['username'] = username
            session['username'] = username
            session['password'] = password
            return redirect(url_for('token_input', username=username))
        else:
            flash("아이디 혹은 비밀번호를 확인해주세요!")
    return render_template('login.html')


# registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 데이터베이스 연결
        conn = sqlite3.connect('dic_sumbot.db')
        cursor = conn.cursor()
        # 사용자 정보 삽입
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        # 변경 사항 저장
        conn.commit()
        # 연결 종료
        conn.close()
        flash('가입이 완료되었습니다. 로그인해주세요!')
        return redirect(url_for('login', username=username))
    return render_template('register.html')

# token_input
@app.route('/token_input', methods=['GET', 'POST'])
def token_input():
    user_name = request.args.get('username')
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        bot_name = request.form['bot_name']
        token_value = request.form['token_value']
        session['token_value'] = token_value
        session['bot_name'] = bot_name
        username = session.get('username')
        # 현재 날짜 및 시간 가져오기
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 데이터베이스 연결
        connection = sqlite3.connect('dic_sumbot.db')
        cursor = connection.cursor()

        # users 테이블에 토큰 값 저장
        cursor.execute('UPDATE users SET token = ? WHERE username = ? AND password = ?', (token_value, session['username'], session['password']))
        cursor.execute('INSERT OR IGNORE INTO sum_message (token) VALUES (?)', (token_value,))

        # sum_audio 테이블에 토큰 저장
        cursor.execute('UPDATE sum_message SET token = ? WHERE token = ?', (token_value, session['token_value']))

        # 변경 사항 저장 및 연결 종료
        connection.commit()
        connection.close()
        return redirect(url_for('run_bot', bot_name=bot_name, username=username))

    return render_template('token_input.html', username=user_name)

@app.route('/run_bot', methods=['GET', 'POST'])
def run_bot():
    bot_name = session.get('bot_name')
    username = session.get('username')
    if request.method == 'POST':
        flag = request.form.get('flag')
        token = session.get('token_value')

        # Bot start/end
        if flag == 'start' or flag == 'end':
            if flag == 'start':
                if token in subprocesses:
                    flash('이미 실행 중입니다!')
                    print('이미 실행 중입니다!')
                else:
                    subprocesses[token] = subprocess.Popen(['python', 'DiscordBot.py', token])
                    flash('봇이 시작되었습니다!')
                    print('봇이 시작되었습니다!')
            elif flag == 'end':
                if token in subprocesses:
                    subprocesses[token].terminate()
                    del subprocesses[token]
                    flash('봇이 종료되었습니다!')
                    print('봇이 종료되었습니다!')
                else:
                    flash('봇이 실행 중이 아닙니다!')
                    print('봇이 실행 중이 아닙니다!')
            return render_template('run_bot.html', bot_name=bot_name, username=username)

        # Audio upload
        elif flag == 'upload':
            audio_file = request.files.get('file')
            if audio_file:
                connection = sqlite3.connect('dic_sumbot.db')
                cursor = connection.cursor()

                audio_file.save('received_audio.wav')
                summarize = summarize_audio('received_audio.wav')
                flash('음성이 녹음되었습니다!')
                
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute('INSERT INTO users (token, date, summarize) VALUES (?, ?, ?)', (token, date, summarize))
                cursor.execute('INSERT INTO sum_message (token, summarize) VALUES (?, ?)', (token, summarize))
                
                connection.commit()
                connection.close()
            else:
                flash('녹음 파일이 없습니다!')
        
        # Raspberry Pi recording
        elif flag == 'rasp_start' or flag == 'rasp_stop':
            data = {'token': token}
            rasp_url = f'http://192.168.137.33:9999/{flag.split("_")[1]}'
            response = requests.post(rasp_url, data=data)
            flash(response.text)

        return render_template('run_bot.html', bot_name=bot_name, username=username)

    return render_template('run_bot.html', bot_name=bot_name, username=username)

#오디오를 받았을 때 음성인식 및 요약
@app.route('/upload_audio', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return 'No audio file part'
    audio_file = request.files['audio']
    token = request.form.get('token')
    print(token)
    if audio_file.filename == '':
        return 'No selected file'
    connection = sqlite3.connect('dic_sumbot.db')
    cursor = connection.cursor()

    audio_file.save('received_audio.wav')
    summarize = summarize_audio('received_audio.wav')
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('INSERT INTO users (token, date, summarize) VALUES (?, ?, ?)', (token, date, summarize))
    cursor.execute('INSERT INTO sum_message (token, summarize) VALUES (?, ?)', (token, summarize))
    
    connection.commit()
    connection.close()
    
    return 'File uploaded successfully'


atexit.register(cleanup_subprocesses)

if __name__ == '__main__':
    create_table()
    app.run('0.0.0.0', port=5000, debug=True)
    
