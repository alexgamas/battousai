'''
                                BEGIN OF PROGRAM
----------------------------------------------------------------------------
AUTHOR     : Alex Gamas
MAIN GOAL  :
VERSION    : 0.0.2
USAGE TIPS :
----------------------------------------------------------------------------

'''

import pygame
import Image
from pygame.locals import *
import time

img_name = "i3.jpg"
img = Image.open(img_name)

width = 800
height = 600
to_size = (width, height)


_BLUE = (0,0,255)
_RED  = (255,0,0)
mode = Image.ANTIALIAS
''' Modes:
Image.ANTIALIAS
Image.NEAREST
Image.BILINEAR
Image.BICUBIC
'''

img_resized = img.resize(to_size, mode)

''' SAVE IMAGE RESIZED '''
'''
img_resized.save("20110914222310.00001234.jpg")
'''

pygame.init()
window = pygame.display.set_mode(to_size)
pygame.display.set_caption("Imagem: " + img_name)
screen = pygame.display.get_surface()


pg_img = pygame.image.frombuffer(img_resized.tostring(), to_size, img.mode)


					
first_point = (0, 0)
last_point  = (0, 0)
click = False
square_by_size = (0, 0, 0, 0)

screen.blit(pg_img, (0,0))
pygame.display.update()

#pygame.mouse.set_visible(False)


while True:
	#iniTime = time.time()
	
	events = pygame.event.get()
	for event in events:
		if (event.type == QUIT):
			exit()
		elif (event.type == MOUSEMOTION):
			pos = event.pos
			btns = event.buttons
						
		elif (event.type == MOUSEBUTTONUP):
			pos = event.pos
			button = event.button
			
			if (button == 1):
				if (click):
					last_point = pos
					print "Last Point: ", last_point
					click = False

					''' COORDINATE ORDENATION '''					
					x1 = min(first_point[0], last_point[0])
					y1 = min(first_point[1], last_point[1])
					x2 = max(first_point[0], last_point[0])
					y2 = max(first_point[1], last_point[1])

					w = x2 - x1
					h = y2 - y1
					
					square_by_cord = (x1, y1, x2, y2)
					square_by_size = (x1, y1, w, h)
					
					pygame.draw.rect(window, _BLUE, square_by_size, 1)
					pygame.display.update()
					
					out_img = img_resized.crop(square_by_cord)
					timestamp = time.time()
					
					img_out_name = "out_images/" + str(timestamp) + ".png"
					print "Saving ... ", img_out_name, square_by_cord
					out_img.save(img_out_name, "PNG")
					
				else:
					first_point = pos
					print "First Point: ", first_point

					screen.blit(pg_img, (0,0))
					pygame.display.update()

					if (max(square_by_size) > 0):
						
						sample_square = (first_point[0], first_point[1], w, h)
						print "Sample square: ", sample_square
						pygame.draw.rect(window, _RED, sample_square, 1)
						pygame.display.update()
					
					click = True
			elif (button == 3):
				print "Reset Coord."
				first_point = (0, 0)
				last_point  = (0, 0)

				click = False
				
'''END OF PROGRAM
'''
