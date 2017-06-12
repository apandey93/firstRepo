import random
import pygame as pg
from . import constants as c
from random import shuffle

class CollisionHandler(object):
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

    def update(self, keys, current_time):
        """
        Check for collisions between game objects.
        """
        self.blockers = self.make_blocker_list(self.static_blockers,
                                               self.sprites)
        self.player.rect.move_ip(self.player.x_vel, self.player.y_vel)
	self.check_listoption()
        self.check_for_blockers()
        for sprite in self.sprites:
            sprite.rect.move_ip(sprite.x_vel, sprite.y_vel)
        self.check_for_blockers()
        if self.player.rect.x % 32 == 0 and self.player.rect.y % 32 == 0:
            if not self.player.state == 'resting':
                self.check_for_portal()
                self.check_for_battle()
            self.player.begin_resting()

        for sprite in self.sprites:
            if sprite.state == 'automoving':
                if sprite.rect.x % 32 == 0 and sprite.rect.y % 32 == 0:
                    sprite.begin_auto_resting()

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
    def check_listoption(self):
	options=('left','down','up','right')
	goodoptions=[]
	for option in options:
		futurex=self.player.rect.left
		futurey=self.player.rect.top
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
	self.player.setposiblemoves(goodoptions)

    def check_for_portal(self):
        """
        Check for a portal to change level scene.
        """
        portal = pg.sprite.spritecollideany(self.player, self.portals)

        if portal:
            self.level.use_portal = True
            self.level.portal = portal.name

    def check_for_blockers(self):
        """
        Checks for collisions with blocker rects.
        """
        player_collided = False
        sprite_collided_list = []
        for blocker in self.blockers:
            if self.player.rect.colliderect(blocker):
                player_collided = True

        if player_collided:
            self.reset_after_collision(self.player)
            self.player.begin_resting()

        for sprite in self.sprites:
            for blocker in self.static_blockers:
                if sprite.rect.colliderect(blocker):
                    sprite_collided_list.append(sprite)
            if sprite.rect.colliderect(self.player.rect):
                sprite_collided_list.append(sprite)
            sprite.kill()
            if pg.sprite.spritecollideany(sprite, self.sprites):
                sprite_collided_list.append(sprite)
            self.sprites.add(sprite)
            for blocker in sprite.wander_box:
                if sprite.rect.colliderect(blocker):
                    sprite_collided_list.append(sprite)


        for sprite in sprite_collided_list:
            self.reset_after_collision(sprite)
            sprite.begin_auto_resting()

    def reset_after_collision(self, sprite):
        """Put player back to original position"""
        if sprite.x_vel != 0:
                sprite.rect.x -= sprite.x_vel
        else:
            sprite.rect.y -= sprite.y_vel

    def check_for_battle(self):
        """
        Switch scene to battle 1/5 times if battles are allowed.
        """
        if self.level.allow_battles:
            self.level.game_data['battle counter'] -= 5
            if self.level.game_data['battle counter'] <= 0:
                self.level.switch_to_battle = True



