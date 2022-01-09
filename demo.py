# 引入pygame和sys
import pygame
import sys 
import os
import time

global screen

def draw_time():
	localtime = time.localtime()
	date_str = time.strftime("%Y 年 %m 月 %d 日", localtime)
	hm_str = time.strftime("%H:%M", localtime)
	second_str = time.strftime("%S", localtime)

	my_font = pygame.font.Font('font.ttf', 20)
	text_fmt = my_font.render(date_str, 1, (255,255,255))
	screen.blit(text_fmt, (10,10))

	text_fmt = my_font.render(hm_str, 1, (255,255,255))
	text_width, text_height = my_font.size(hm_str)
	screen.blit(text_fmt, (240,10))

	my_font = pygame.font.Font('font.ttf', 14)
	text_fmt = my_font.render(second_str, 1, (255,255,255))
	screen.blit(text_fmt, (240+text_width+10,17))

# 定义一个run_game函数，把初始化的逻辑都放里面
def run_game():
	# 初始化pygame引擎
	pygame.init()
	# 设置pygame窗口大小，如果设置为0,0则自动识别分辨率，相当于窗口最大化
	global screen
	screen = pygame.display.set_mode((600,400))
	
	# 无限循环，游戏的主循环
	while True:
		# 监听消息
		for event in pygame.event.get(): 
			# 当监听到pygame的退出时，触发sys.exit退出应用
			if event.type == pygame.QUIT:
				sys.exit()
		# 刷新屏幕
		screen.fill((0,0,0))

		draw_time()
		pygame.display.update() 

# 执行run_game函数
run_game()