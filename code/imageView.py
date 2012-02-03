# -*- coding: utf-8 -*-

'''
BEGIN OF PROGRAM
----------------------------------------------------------------------------
AUTHOR	 : Alex Gamas
MAIN GOAL  : Open an Image file and display this!
VERSION	: 0.0.2
USAGE TIPS :
----------------------------------------------------------------------------
'''

import pygame
from pygame.locals import *
import battousaiUtil as util

class Selection():
	_p1 = (0, 0)
	_p2 = (0, 0)
	_w = 0
	_h = 0
	_sel_type = 0
	def square_by_coord(self):
		pass
	def squareBySize(self):
		return (self._p1[0], self._p1[1], self._w, self._h)
	def __init__(self, points, sel_type):
		self._p1 = (points[0], points[1])
		self._p2 = (points[2], points[3])
		self._w = points[2] - points[0] 
		self._h = points[3] - points[1]
		self._sel_type = sel_type

class ImageView():
	__RED = (255, 000, 000)
	__GREEN = (000, 255, 000)
	__BLUE = (000, 000, 255) 

	selections = []
	clickPoints = []

	def addClickPoint(self, point):
		self.clickPoints.append(point)
		if len(self.clickPoints) == 2:
			self.addSubSelection(self.clickPoints)
			self.clickPoints = []

	def addSubSelection(self, clicks):
		x1 = min(clicks[0][0], clicks[1][0])
		x2 = max(clicks[0][0], clicks[1][0])
		y1 = min(clicks[0][1], clicks[1][1])
		y2 = max(clicks[0][1], clicks[1][1])
		
		color = self.__RED
		if (self.fieldMark):
			print "xxx"
			color = self.__BLUE
			
		sel_type = 12
		
		sel = Selection((x1, y1, x2, y2), sel_type)
		self.selections.append(sel)
		rect = sel.squareBySize()
		
		pygame.draw.rect(self.window, color, rect, 1)
		self.display.update()

	def showImage(self, imageFilename):
		self.updateTitle()
		image = pygame.image.load(imageFilename)
		self.screen.blit(image, (0, 0))
		self.display.update()

	def close(self):
		exit()

	def handleMouseMotion(self, position):
		pass

	def handleMouseButton(self, position, button):
		if button == 1:
			self.addClickPoint(position)

	def handleKey(self, key, modifier):
		if key in (K_q, K_ESCAPE):
			self.close()
		elif key == K_r:
			print "recording ..."
			
			
		elif key == K_f:
			self.fieldMark = not self.fieldMark
			if self.fieldMark:
				print "Field Mark [ X ]"
			else:
				print "Field Mark [   ]"
				
				
				#dar repaint aki para que os fields sejam reorganizados....
				
			return
		filelen = len(self.files)
					
		if (self.filepos != None):			
			if (filelen > 0):
				if key == K_d:
					self.filepos = self.filepos + 1
					if self.filepos >= filelen:
						self.filepos = 0
				elif key == K_a:
					self.filepos = self.filepos - 1
					if self.filepos < 0:
						self.filepos = filelen - 1
				#----------
				self.atualFile = self.files[self.filepos]
				self.showImage(self.atualFile)
			else:
				print "Lista Vazia!"
		else:
			print "GO! GO! GO!"
			self.filepos = 0
			self.atualFile = self.files[self.filepos]
			self.showImage(self.atualFile);
	
	def deliverEvents(self, event):
		
		'''
		Eventos possíveis
		--------------------------------------
		QUIT		none
		ACTIVEEVENT	gain, state
		KEYDOWN		unicode, key, mod
		KEYUP		key, mod
		MOUSEMOTION	pos, rel, buttons
		MOUSEBUTTONUP   pos, button
		MOUSEBUTTONDOWN pos, button
		JOYAXISMOTION   joy, axis, value
		JOYBALLMOTION   joy, ball, rel
		JOYHATMOTION	joy, hat, value
		JOYBUTTONUP	joy, button
		JOYBUTTONDOWN   joy, button
		VIDEORESIZE	size, w, h
		VIDEOEXPOSE	none
		USEREVENT       code
		--------------------------------------
		'''

		# - Eventos necessários - #
		if (event.type == QUIT):
			self.close()
		elif (event.type == MOUSEMOTION):
			self.handleMouseMotion(event.pos)			
		elif (event.type == MOUSEBUTTONUP):
			self.handleMouseButton(event.pos, event.button)
		elif (event.type == KEYUP):
			self.handleKey(event.key, event.mod)
		# - Eventos necessários - #
	def updateTitle(self):
		self.display.set_caption("Imagem: " + str(self.atualFile))
		
	def __init__(self, files):
		# Passa a lista de arquivos para a classe;
		self.files = files
		self.filepos = None
		self.atualFile = None
		
		# flag vars
		self.record = False
		self.fieldMark = False
		# /flag vars
		
		# Inicia o grafico e entrega os handlers de evento

		pygame.init()
		self.screen_size = (800, 600);
		self.display = pygame.display
		self.window = self.display.set_mode(self.screen_size)
		self.screen = self.display.get_surface()
		self.updateTitle()
		
		pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))
		
		self.display.update()
		while True:
			events = pygame.event.get()
			for event in events:
				self.deliverEvents(event)
		
		# Inicia o grafico e entrega os handlers de evento
		
'''END OF PROGRAM
'''
