import sys
import os
import pygame
import requests
import threading
import time
import socket

# 全局变量
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 400
BG_COLOR = (0,0,0)
TIME_SECOND = 0
CUR_PATH = os.path.split(os.path.realpath(__file__))[0]
FONT_PATH = CUR_PATH+'/font.ttf'

# bilibili
REQUEST_INTERVAL = 5

BILI_MID = "422646817"
BILI_LIVEID = "21759271"
BILI_SESSDATA = "3ea2cef8%2C1656552588%2C5d28d%2A11"

BILI_UNREAD = 0  #未读消息
BILI_LIVEONLINE = 0  #直播人气
BILI_TOTALFANS = 0  #粉丝数
BILI_TOTALVIEW = 0  #总播放
BILI_TOTALLIKE = 0 #总获赞
BILI_TOTALELEC = 0 #总充电

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
 
    return ip

def getBilibiliFansCount():
    global BILI_TOTALFANS
    global BILI_UNREAD
    global BILI_LIVEONLINE
    global BILI_TOTALELEC
    global BILI_TOTALLIKE
    global BILI_TOTALVIEW
    try:
        res = requests.get('https://api.bilibili.com/x/relation/stat?vmid='+BILI_MID)
        data = res.json()
        
        BILI_TOTALFANS = data['data']['follower']
    except:
        BILI_TOTALFANS = 0

    try:
        res = requests.get('http://api.bilibili.com/x/msgfeed/unread',headers={
            'Cookie':'SESSDATA='+BILI_SESSDATA
        })
        data = res.json()
        BILI_UNREAD = data['data']['at']+data['data']['chat']+data['data']['like']+data['data']['reply']+data['data']['sys_msg']+data['data']['up']
    except:
        BILI_UNREAD = 0

    try:
        res = requests.get('https://api.bilibili.com/x/space/acc/info?mid='+BILI_MID)
        data = res.json()
        BILI_LIVEID = data['data']['live_room']['roomid']
        BILI_LIVEONLINE = data['data']['live_room']['online']
    except:
        BILI_LIVEONLINE = 0

    # try:
    #     res = requests.get('http://api.bilibili.com/x/space/upstat', cookies={
    #         'SESSDATA':BILI_SESSDATA
    #     }, data={
    #         'mid':BILI_MID
    #     })
    #     data = res.json()
    #     print(data)
    #     BILI_TOTALVIEW = data['data']['archive']['view']
    #     BILI_TOTALLIKE = data['data']['likes']
    # except:
    #     BILI_TOTALVIEW = 0
    #     BILI_TOTALLIKE = 0

    try:
        res = requests.get('https://api.bilibili.com/x/ugcpay-rank/elec/month/up?up_mid='+BILI_MID)
        data = res.json()
        BILI_TOTALELEC = data['data']['total']
    except:
        BILI_TOTALELEC = 0

def getLiveRoomChat():
    # https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid=
    print(BILI_LIVEID)
    try:
        res = requests.get('https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid='+BILI_LIVEID)
        data = res.json()
        
        print(data['data']['room'])
    except:
        print("报错了")

def requestBiliData():
    getBilibiliFansCount()
    # getLiveRoomChat()

def draw_time():
    date_str = time.strftime("%Y 年 %m 月 %d 日", time.localtime())
    hm_str = time.strftime("%H %M", time.localtime())
    second_str = time.strftime("%S", time.localtime())

    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render(date_str, 1, (255,255,255))
    screen.blit(text_fmt, (10,10))

    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render(hm_str, 1, (255,255,255))
    screen.blit(text_fmt, (240,10))

    if TIME_SECOND%2==0:
        my_font = pygame.font.Font(FONT_PATH, 20)
        text_fmt = my_font.render(":", 1, (255,255,255))
        screen.blit(text_fmt, (262,10))

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
    # 绘制小破站Logo
    screen.blit(image_logo, (30,50))
    # 绘制粉丝数
    my_font = pygame.font.Font(FONT_PATH, 220)
    text_fmt = my_font.render(str(BILI_TOTALFANS), 1, (255,255,255))
    screen.blit(text_fmt, (380,60))
    # 绘制其他信息 " 总播放："+str(BILI_TOTALVIEW)+" 总获赞："+str(BILI_TOTALLIKE)+
    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render("未读消息："+str(BILI_UNREAD), 1, (255,255,255))
    text_width, text_height = my_font.size("未读消息："+str(BILI_UNREAD))
    screen.blit(text_fmt, (10,SCREEN_HEIGHT-10-text_height))

    totalstr = " 总充电："+str(BILI_TOTALELEC)+" 直播人气："+str(BILI_LIVEONLINE)
    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render(totalstr, 1, (255,255,255))
    text_width, text_height = my_font.size(totalstr)
    screen.blit(text_fmt, (SCREEN_WIDTH-10-text_width,SCREEN_HEIGHT-10-text_height))

def game_loop():
    #绘制底色
    screen.fill(BG_COLOR)

    global TIME_SECOND

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == SECOND_EVT:
            TIME_SECOND+=1
            if TIME_SECOND%REQUEST_INTERVAL==0:
                requestBiliData()
            
    # 视图层构建区

    draw_time()
    draw_ip()
    draw_bilibili()
    
    # 刷新识图
    pygame.display.update()

def run_game():
    pygame.init()
    pygame.mouse.set_visible(0)

    global screen
    screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
    # pygame.display.toggle_fullscreen()

    # 定义记秒事件
    global SECOND_EVT
    SECOND_EVT = pygame.USEREVENT +1
    pygame.time.set_timer(SECOND_EVT,1000)

    global image_logo
    image_logo = pygame.image.load(CUR_PATH+"/icon_bilibili.jpg")
    image_logo = pygame.transform.scale(image_logo, (300, 300))

    requestBiliData()

    # game loop
    while True:
        game_loop()

run_game()