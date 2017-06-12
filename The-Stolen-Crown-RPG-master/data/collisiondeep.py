import random
import pygame as pg
from . import constants as c
from random import shuffle

class CollisionHandlerdeep(object):
    """Handles collisions between the user, blockers and computer
    characters"""
    def __init__(self, player, blockers, sprites, portals, level):
        self.player = player
        self.static_blockers = blockers
        self.blockers = self.make_blocker_list(blockers, sprites)
        self.sprites = sprites
        self.portals = portals
        self.level = level

    def make_blocker_list(self, blockers, sprites):
        """
        Return a combined list of sprite blockers and object blockers.
        """
        blocker_list = []

        for blocker in blockers:
            blocker_list.append(blocker)

        for sprite in sprites:
            blocker_list.extend(sprite.blockers)
     
	return blocker_list
    def blocker_list(self):
        """
        Return a combined list of sprite blockers and object blockers.
        """
     
	return self.blockers

    def future_positiony(self, x,option):
	futurex=x	
	if option=='up':
		futurex-=1
	if option=='down':
		futurex+=1
	return futurex

    def future_positionx(self, y,option):
	futurey=y	
	if option=='left':
		futurey-=1
	if option=='right':
		futurey+=1
	return futurey
    def check_listoption(self,x,y):
	options=('up','down','left','right')
	goodoptions=[]
	for option in options:
		futurex=x
		futurey=y
		goodoption=True
		portal=False
		for i in  range(0, 32):
			futurex=self.future_positionx(futurex,option)
			futurey=self.future_positiony(futurey,option)
			futurepos=pg.Rect(futurex,futurey,32,32)
			for blocker in self.blockers:
				if futurepos.colliderect(blocker):
					goodoption=False
					break
			for portal in self.portals:
				if futurepos.colliderect(portal):
					goodoption=True
					portal=True
					break
			if portal:
				break
			if not goodoption:
				break
		if goodoption:
			goodoptions.append(option)
	return goodoptions


