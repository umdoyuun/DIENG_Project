import discord
from discord.ext import commands
import asyncio
import re
import sqlite3
import sys
import datetime

#DB 켜기
connection = sqlite3.connect('dic_sumbot.db')
cursor = connection.cursor()
#cursor.execute('CREATE TABLE IF NOT EXISTS users (token TEXT, username TEXT, password TEXT, date TEXT, summarize TEXT)')
#cursor.execute('CREATE TABLE IF NOT EXISTS sum_message (token TEXT, summarize TEXT)')

TOKEN = sys.argv[1]
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_close():
    print(f'{bot.user.name}이 종료 됩니다.')
    connection.close()

# 디스코드 봇이 접속한 서버에서 가장 낮은 텍스트 채널을 찾는 함수
def get_lowest_text_channel():
    lowest_channel = None
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if lowest_channel is None or channel.id < lowest_channel.id:
                lowest_channel = channel
    return lowest_channel

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    lowest_channel = get_lowest_text_channel()
    if lowest_channel:
        await lowest_channel.send(f'안녕하세요!\n {bot.user.name} 수업 자동 요약봇입니다!')
    bot.loop.create_task(my_back_ground_task())

#cursor.execute('CREATE TABLE IF NOT EXISTS users (token TEXT, username TEXT, password TEXT, date TEXT, summarize TEXT)')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    channel = message.channel
    content = message.content
    if "월" in content and "일" in content:
        month_match = re.search(r'(\d?\d{1,2})월', content)
        day_match = re.search(r'(\d?\d{1,2})일', content)
        month = month_match.group(1)
        day = day_match.group(1)
        if 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
            current_year = datetime.datetime.now().year
            date = f"{int(month):02d}-{int(day):02d}"
            print(date)
            cursor.execute('SELECT summarize FROM users WHERE token=? AND date LIKE ?',(TOKEN, f'%{date}%'))
            result = cursor.fetchall()
            print(result)
            if result:
                for i in range(len(result)):
                    msg = result[i][0]  # 각 레코드에서 필드를 추출합니다.
                    await channel.send(msg)
                    print("디스코드 채널로 메시지 전송 완료:", msg)
            else:
                await channel.send('해당 날짜의 요약본이 없습니다.')
        else:
            await channel.send("1잘못된 입력입니다.\n'X월 X일의 요약본을 줘' 등의 형식으로 입력해주세요")
    else:
        await channel.send("2잘못된 입력입니다.\n'X월 X일의 요약본을 줘' 등의 형식으로 입력해주세요")

# send_summary_to_channel 함수 수정
async def my_back_ground_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        cursor.execute('SELECT summarize FROM sum_message WHERE token=?',(TOKEN, ))
        result = cursor.fetchall()
        if result:
            lowest_channel = get_lowest_text_channel()
            if lowest_channel:
                for record in result:
                    for field in record:
                        if field:
                            await lowest_channel.send(str(field))
                            print("디스코드 채널로 메시지 전송 완료:", field)
                cursor.execute('DELETE FROM sum_message WHERE token=?',(TOKEN, ))
                connection.commit()
        await asyncio.sleep(20)

bot.run(TOKEN)