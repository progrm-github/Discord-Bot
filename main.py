import discord
from discord.ext import commands
import youtube_dl
import csv
import pandas as pd
import os
import re
from collections import OrderedDict

bot = commands.Bot(command_prefix='>')
f = open('database.csv', 'w', encoding='utf-8', newline='\n')
wr = csv.writer(f)
m=0
while m<1:
    m=1
    wr.writerow(['mal', 'mal1'])
    f.close()

@bot.command()
async def 초기화(ctx, id, pw):
    if id == 'jm0730':
        if pw == 'jmjmjm0730':
            await ctx.send('데이터베이스를 초기화합니다.')
            f = open('database.csv', 'w', encoding='utf-8', newline='\n')
            wr = csv.writer(f)
            wr.writerow(['mal', 'mal1'])
            f.close()
        else:
            await ctx.send('비밀번호가 잘못되었습니다.')
    else:
        await ctx.send('ID가 잘못되었습니다.')

@bot.command()
async def 도움(ctx): 
    await ctx.send('명령어 설명\n\n>배워 [대상] [설명]\n대상에 대해 배웁니다.\n\n>말해 [대상]\n배운 대상에 대해 말합니다.\n\n>핑\n봇의 핑을 확입합니다.\n\n>재생 [Youtube URL]\n유튜브 노래를 재생합니다.\n\n>일시정지\n노래를 일시정지 합니다.\n\n>다시시작\n노래를 다시 시작합니다.\n\n>멈춰\n노래를 멈춥니다.\n\n>나가\n봇이 음성채널에서 나갑니다.')     
@bot.command()
async def 배워(ctx, mal, mal1):
    text_mod = re.sub('[^정지민]','',mal)
    text_mod1 = re.sub('[^정지민]','',mal1)
    a_str = text_mod
    a_str1 = text_mod1
    if '정지민' in ''.join(OrderedDict.fromkeys(a_str)):
        await ctx.send('정지민이 들어간 말은 배울 수 없어요!')
        await ctx.send('https://media.tenor.com/images/bc112882a77db08c53e072765be4fe1e/tenor.gif')
    elif '정지민' in ''.join(OrderedDict.fromkeys(a_str1)):
        await ctx.send('정지민이 들어간 말은 배울 수 없어요!')
        await ctx.send('https://media.tenor.com/images/bc112882a77db08c53e072765be4fe1e/tenor.gif')
    else:
        f = open('database.csv', 'a', encoding='utf-8', newline='\n')
        wr = csv.writer(f)
        wr.writerow([mal, mal1])
        f.close()
        await ctx.send(mal + ' 이/가 ' + mal1 + '이라구요? 기억했어요.')

@bot.command()
async def 말해(ctx, mall1):
    abc = pd.read_csv('database.csv')
    df = pd.DataFrame(abc)
    aabb = df[df['mal'] == mall1]
    aabbb = str(aabb).split(' ')
    await ctx.send(aabbb[-1])

@bot.command()
async def 핑(ctx):
    await ctx.send('퐁! {0}'.format(round(bot.latency, 1)))

@bot.command()
async def 재생(ctx, url):
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
    	await channel.connect()
    	await ctx.send(str(bot.voice_clients[0].channel) + "에 연결되었어요.")

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    await ctx.send("현재 재생중 :" + url)
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def ㅍ(ctx, url):
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
    	await channel.connect()
    	await ctx.send(str(bot.voice_clients[0].channel) + "에 연결되었어요.")

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    await ctx.send("현재 재생중 :" + url)
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def 일시정지(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("이미 멈춰 있어요.")

@bot.command()
async def 다시시작(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
        await ctx.send("이미 재생중이에요.")
        
@bot.command()
async def 멈춰(ctx):
    if bot.voice_clients[0].is_playing():
    	bot.voice_clients[0].stop()
    else:
    	await ctx.send("재생중이 아니에요.")

@bot.command()
async def 나가(ctx):
    if bot.voice_clients[0].is_playing():
        await bot.voice_clients[0].disconnect()
        

bot.run('Token')
