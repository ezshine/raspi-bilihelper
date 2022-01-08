import sys
import os
import pygame
from threading import Thread
import time
import socket
import pyttsx3
import httpx
import asyncio
import json

# 全局变量
TIME_SECOND = 0
CUR_PATH = os.path.split(os.path.realpath(__file__))[0]
FONT_PATH = CUR_PATH+'/font.ttf'

# 屏幕尺寸和画布背景色
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 400
BG_COLOR = (0,0,0)

# 轮询间隔
REQUEST_INTERVAL = 5

# 哔哩哔哩配置
BILI_MID = "422646817"
BILI_LIVEID = "21759271"

# 从B站cookie里获取
BILI_SESSDATA = "3ea2cef8%2C1656552588%2C5d28d%2A11"

# bilibili
BILI_UNREAD = 0  #未读消息
BILI_LIVEONLINE = 0  #直播人气
BILI_TOTALFANS = 0  #粉丝数
BILI_TOTALVIEW = 0  #总播放
BILI_TOTALLIKE = 0 #总获赞
BILI_TOTALELEC = 0 #总充电

DANMU_ISSHOW = 0
DANMU_ISRUNNING = 0
DANMU_TEXT = ''
DANMU_X = 0

# TTS
engine = pyttsx3.init()
engine.setProperty('rate', 140)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
 
    return ip

async def getBilibiliFansCount():
    global BILI_TOTALFANS
    global BILI_UNREAD
    global BILI_LIVEID
    global BILI_LIVEONLINE
    global BILI_TOTALELEC
    global BILI_TOTALLIKE
    global BILI_TOTALVIEW
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post('https://e0b75de1-90c7-4c11-9d12-a8bc84c4d081.bspapp.com/http/bilibili',data=json.dumps({
                "mid":BILI_MID,
                "sessdata":BILI_SESSDATA,
                "action":"getinfo"
            }),headers={
                "Content-Type": "application/json; charset=UTF-8"
            })
            data = res.json()
            
            BILI_UNREAD = data['data']['unread']['at']+data['data']['unread']['chat']+data['data']['unread']['like']+data['data']['unread']['reply']+data['data']['unread']['sys_msg']+data['data']['unread']['up']
            BILI_TOTALELEC = data['data']['total']['elec']
            BILI_TOTALFANS = data['data']['total']['follower']
            BILI_TOTALLIKE = data['data']['total']['like']
            BILI_TOTALVIEW = data['data']['total']['view']
            BILI_LIVEONLINE = data['data']['liveroom']['online']
            BILI_LIVEID = str(data['data']['liveroom']['roomid'])
    except:
        print("err")

async def getLiveRoomChat():
    global DANMU_ISSHOW
    global DANMU_LAST
    global DANMU_TEXT
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get('https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid='+BILI_LIVEID)
            data = res.json()

            room = data['data']['room']
            if len(room)>0:
                last_danmu = room[len(room)-1]
                last_danmu_time = time.mktime(time.strptime(last_danmu['timeline'], "%Y-%m-%d %H:%M:%S"))
                if 'DANMU_LAST' in globals():
                    if DANMU_LAST == last_danmu:
                        return None
                if last_danmu_time>time.time()-300 and last_danmu['uid']!=BILI_MID:
                    DANMU_LAST = last_danmu
                    DANMU_TEXT = last_danmu['nickname']+"说"+last_danmu['text']
                    DANMU_ISSHOW = 1
    except Exception as e:
        print(e)

def draw_danmu():
    global DANMU_ISRUNNING
    global DANMU_ISSHOW
    global DANMU_X
    global DANMU_TEXT

    if DANMU_ISRUNNING==1:
        my_font = pygame.font.Font(FONT_PATH, 220)
        text_fmt = my_font.render(DANMU_TEXT, 1, (255,255,255))
        text_width, text_height = my_font.size(DANMU_TEXT)
        screen.blit(text_fmt, (DANMU_X,(SCREEN_HEIGHT-text_height)/2))
        DANMU_X-=10
        if DANMU_X<-text_width:
            DANMU_ISSHOW = 0
            DANMU_ISRUNNING = 0
    else:
        DANMU_ISRUNNING = 1
        DANMU_X = SCREEN_WIDTH
        # 在子线程里TTS
        Thread(target=pyttsx3.speak,args=(DANMU_TEXT,)).start()


def requestBiliData():
    asyncio.run(getBilibiliFansCount())
    asyncio.run(getLiveRoomChat())

def draw_time():
    date_str = time.strftime("%Y 年 %m 月 %d 日", time.localtime())
    hm_str = time.strftime("%H:%M", time.localtime())
    second_str = time.strftime("%S", time.localtime())

    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render(date_str, 1, (255,255,255))
    screen.blit(text_fmt, (10,10))

    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render(hm_str, 1, (255,255,255))
    text_width, text_height = my_font.size(hm_str)
    screen.blit(text_fmt, (240,10))

    my_font = pygame.font.Font(FONT_PATH, 14)
    text_fmt = my_font.render(second_str, 1, (255,255,255))
    screen.blit(text_fmt, (240+text_width+10,17))

def draw_ip():
    try:
        ip_str = get_host_ip()
    except:
        ip_str = ""
    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render(ip_str, 1, (255,255,255))
    text_width, text_height = my_font.size(ip_str)
    screen.blit(text_fmt, (SCREEN_WIDTH-text_width-10,10))

def draw_bilibili():
    # 绘制粉丝数
    my_font = pygame.font.Font(FONT_PATH, 220)
    text_fmt = my_font.render(str(BILI_TOTALFANS), 1, (255,255,255))
    text_width, text_height = my_font.size(str(BILI_TOTALFANS))
    text_x = (SCREEN_WIDTH-text_width)/2
    text_y = (SCREEN_HEIGHT-text_height)/2
    screen.blit(text_fmt, (text_x+160,text_y))

    # 绘制小破站Logo
    screen.blit(image_logo, (text_x-160,text_y-10))
    
    # 绘制其他信息 " 总播放："+str(BILI_TOTALVIEW)+" 总获赞："+str(BILI_TOTALLIKE)+
    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render("未读消息："+str(BILI_UNREAD), 1, (255,255,255))
    text_width, text_height = my_font.size("未读消息："+str(BILI_UNREAD))
    screen.blit(text_fmt, (10,SCREEN_HEIGHT-10-text_height))

    totalstr = " 总播放："+str(BILI_TOTALVIEW)+" 总获赞："+str(BILI_TOTALLIKE)+" 总充电："+str(BILI_TOTALELEC)+" 直播间人气："+str(BILI_LIVEONLINE)
    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render(totalstr, 1, (255,255,255))
    text_width, text_height = my_font.size(totalstr)
    screen.blit(text_fmt, (SCREEN_WIDTH-10-text_width,SCREEN_HEIGHT-10-text_height))

def game_loop():
    #绘制底色
    screen.fill(BG_COLOR)

    global TIME_SECOND
    global DANMU_ISSHOW

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # sys.exit()
            print('quit')
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        if event.type == SECOND_EVT:
            TIME_SECOND+=1
            if TIME_SECOND%REQUEST_INTERVAL==0 and DANMU_ISSHOW==0:
                requestBiliData()
            
    # 视图层构建区

    if DANMU_ISSHOW==1:
        draw_danmu()
    else:
        draw_time()
        draw_ip()
        draw_bilibili()
    
    # 刷新视图
    pygame.display.update()

def run_game():
    pygame.init()
    # 隐藏鼠标
    pygame.mouse.set_visible(0)

    fpsClock = pygame.time.Clock()

    # 获取系统分辨率
    global screen
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    displayInfo = pygame.display.Info()
    SCREEN_WIDTH = displayInfo.current_w
    SCREEN_HEIGHT = displayInfo.current_h
    
    # 0,0为自动识别系统分辨率
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    # 全屏这个api在树莓派下有点问题
    # pygame.display.toggle_fullscreen()
    

    # 定义记秒事件
    global SECOND_EVT
    SECOND_EVT = pygame.USEREVENT +1
    pygame.time.set_timer(SECOND_EVT,1000)

    global image_logo
    image_logo = pygame.image.load(CUR_PATH+"/icon_bilibili.jpg")
    image_logo = pygame.transform.scale(image_logo, (300, 300))

    requestBiliData()

    # global DANMU_ISSHOW
    # global DANMU_TEXT
    # DANMU_ISSHOW = 1
    # DANMU_TEXT = "哈哈哈哈哈或或"

    # game loop
    while True:
        game_loop()
        fpsClock.tick(30)

run_game()