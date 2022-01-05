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
BILI_ID = "422646817"
BILI_FANSCOUNT = "0"

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
 
    return ip

def getBilibiliFansCount():
    global BILI_FANSCOUNT
    try:
        res = requests.get('https://api.bilibili.com/x/relation/stat?vmid=422646817')
        data = res.json()
        
        BILI_FANSCOUNT = str(data['data']['follower'])
    except:
        BILI_FANSCOUNT = "0"

def draw_time():
    date_str = time.strftime("%Y 年 %m 月 %d 日", time.localtime())
    hm_str = time.strftime("%H:%M", time.localtime())
    second_str = time.strftime("%S", time.localtime())

    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render(date_str, 1, (255,255,255))
    screen.blit(text_fmt, (10,10))

    my_font = pygame.font.Font(FONT_PATH, 20)
    text_fmt = my_font.render(hm_str, 1, (255,255,255))
    screen.blit(text_fmt, (240,10))

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
    
    screen.blit(image_logo, (30,50))

    my_font = pygame.font.Font(FONT_PATH, 220)
    text_fmt = my_font.render(BILI_FANSCOUNT, 1, (255,255,255))
    screen.blit(text_fmt, (380,60))

def game_loop():
    #绘制底色
    screen.fill(BG_COLOR)

    global TIME_SECOND

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == SECOND_EVT:
            TIME_SECOND+=1
            if TIME_SECOND%5==0:getBilibiliFansCount()
            
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

    getBilibiliFansCount()

    # game loop
    while True:
        game_loop()

run_game()