''' Main Game '''

from pygame import *
from pygamehelper import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform
import os

class Door():

    position = vec2d(0, 0)
    door_pos = vec2d(0, 0)
    state = 0
    is_selected = 0
    item = 0

    def __init__(self, item, position):
        self.item = item
        self.state = 1
        self.position = vec2d(415 + 221 * position, 111)
        self.door_pos = self.position
        self.sprite = pygame.image.load(os.path.join("pics", "door.png"))
        self.cart = pygame.image.load(os.path.join("pics", "cart.png"))
        self.goat = pygame.image.load(os.path.join("pics", "goat.png"))
        self.tick = pygame.image.load(os.path.join("pics", "tick.png"))

    def draw(self, screen):
        if self.item:
            screen.blit(self.cart, (self.position[0] - 7, 220))
        else:
            screen.blit(self.goat, (self.position[0] + 20, 220))
        screen.blit(self.sprite, self.position)
        if self.is_selected:
            screen.blit(self.tick, vec2d(self.door_pos[0] + 21, self.door_pos[1] + 40))

    def update(self):
        if self.state == 2:
            if self.door_pos[1] == -109:
                self.state = 3
            else:
                self.door_pos[1] -= 5
        elif self.state == 4:
            if self.door_pos[1] == 111:
                self.state = 1
            else:
                self.door_pos[1] += 5

class Starter(PygameHelper):

    game_state = 0

    score = {"win" : 0, "loose": 0}

    state_2_counter = 50
    state_4_counter = 50

    """
    state 1 : nachalo na igrata - molq izberete si vrata
    state 2 : picha si kazva replikata che shte ni pokaje edna ot drugite i q otvarq
    state 3 : mojem da si promenim izbora

    """

    def reset (self):
        print(self.score)

        self.doors = []

        self.game_state = 0

        self.winner = 0

        self.state_2_counter = 50

        self.state_4_counter = 50

        prize = int(uniform(0, 3))

        for door in range(3):
            if door == prize:
                self.doors.append(Door(1, door))
            else:
                self.doors.append(Door(0, door))

    def run_multiple (self, times, type):
        for x in range(times):
            cart_place = int(uniform(0, 3))
            chose = int(uniform(0, 3))
            izbrana = 5
            for i in range(3):
                if not i==chose and not i==izbrana and not i==cart_place:
                    izbrana = i
            if not type:
                for j in range(3):
                    if not j==chose and not j==izbrana:
                        chose = j
            if chose == cart_place:
                self.score["win"] += 1
            else:
                self.score["loose"] += 1
        print(self.score)
        self.score["win"] = 0
        self.score["loose"] = 0
               
    def run_multiple_tests (self, times, type):
        for p in range(times):
            cart_place = int(uniform(0, 3))
            chose = int(uniform(0, 3))
            if type:
                if cart_place == chose:
                    self.score["win"] += 1
                else:
                    self.score["loose"] += 1
            else:
                if cart_place == chose:
                    self.score["loose"] += 1
                else:
                    self.score["win"] += 1
        print(self.score)        
        self.score["win"] = 0
        self.score["loose"] = 0        
               
    def __init__(self):
        self.w, self.h = 1144, 600


        self.background_bottom = pygame.image.load(os.path.join("pics", "background_bottom.png"))
        self.background_top = pygame.image.load(os.path.join("pics", "background_top.png"))
        self.menu = pygame.image.load(os.path.join("pics", "menu.png"))
        self.presenter = pygame.image.load(os.path.join("pics", "presenter.png"))
        self.speach_bubble = pygame.image.load(os.path.join("pics", "speach_bubble.png"))

        self.state_0_change = pygame.image.load(os.path.join("pics", "text", "state_0_change.png"))
        self.state_0_new = pygame.image.load(os.path.join("pics", "text", "state_0_new.png"))
        self.state_0_save = pygame.image.load(os.path.join("pics", "text", "state_0_save.png"))
        self.state_1_1 = pygame.image.load(os.path.join("pics", "text", "state_1_1.png"))
        self.state_1_2 = pygame.image.load(os.path.join("pics", "text", "state_1_2.png"))
        self.state_1_3 = pygame.image.load(os.path.join("pics", "text", "state_1_3.png"))
        self.state_3_change = pygame.image.load(os.path.join("pics", "text", "state_3_change.png"))
        self.state_3_save = pygame.image.load(os.path.join("pics", "text", "state_3_save.png"))

        self.speach_bubble_1 = pygame.image.load(os.path.join("pics", "speach_bubble_1.png"))
        self.speach_bubble_2 = pygame.image.load(os.path.join("pics", "speach_bubble_2.png"))
        self.speach_bubble_3 = pygame.image.load(os.path.join("pics", "speach_bubble_3.png"))
        self.speach_bubble_4_win = pygame.image.load(os.path.join("pics", "speach_bubble_4_win.png"))
        self.speach_bubble_4_loose = pygame.image.load(os.path.join("pics", "speach_bubble_4_loose.png"))

        self.reset()
        

        self.run_multiple_tests(1000, 0)
        self.run_multiple_tests(1000, 1)
        
        white = (255,255,255)
        PygameHelper.__init__(self, size=(self.w, self.h), fill=(white))
        
    def update(self):
        for door in self.doors:
            door.update()

        if self.game_state == 2:
            if self.state_2_counter == 45:
                # zapochvame da otvarqme vratata
                izbrana = 0
                for door in self.doors:
                    if not door.is_selected and not izbrana and not door.item:
                        izbrana = 1
                        door.state = 2
            if self.state_2_counter == 0:
                self.game_state = 3
            self.state_2_counter -= 1

        if self.game_state == 4:
            if self.state_4_counter == 45:
                # kazvame si replikite i otvarqme neotvorenite vrati
                for door in self.doors:
                    if door.is_selected and door.item:
                        self.score["win"] += 1
                        self.winner = 1
                    elif door.is_selected and not door.item:
                        self.score["loose"] += 1
                        self.winner = 2
                    if door.state == 1:
                        door.state = 2
            if self.state_4_counter == 0:
                self.reset()
            self.state_4_counter -= 1

    
    def mouseUp(self, button, position):
        if position[0] in range(40, 310) and position[1] in range(115, 175):
            if self.game_state == 0:
                self.game_state = 1
            elif self.game_state == 1:
                self.doors[0].is_selected = 1
                self.game_state = 2
            elif self.game_state == 3:
                old_selected = 0
                for door in self.doors:
                    if door.is_selected:
                        old_selected = door
                for new_door in self.doors:
                    if new_door.state == 1 and not new_door.is_selected:
                        old_selected.is_selected = 0
                        new_door.is_selected = 1
                        self.game_state = 4
                        break
            elif self.game_state == 6:
                self.run_multiple_tests(10, 0)
                self.game_state = 0
        elif position[0] in range(40, 310) and position[1] in range(178, 238):
            if self.game_state == 0:
                self.game_state = 6
            elif self.game_state == 1:    
                self.doors[1].is_selected = 1
                self.game_state = 2
            elif self.game_state == 3:
                self.game_state = 4
            elif self.game_state == 6:
                self.run_multiple_tests(10, 1)
                self.game_state = 0
        elif position[0] in range(40, 310) and position[1] in range(241, 301):
            if self.game_state == 1:
                self.doors[2].is_selected = 1
                self.game_state = 2
            elif self.game_state == 6:
                self.run_multiple_tests(100, 0)
                self.game_state = 0
        elif position[0] in range(40, 310) and position[1] in range(304, 364):
            if self.game_state == 6:
                self.run_multiple_tests(100, 1) 
                self.game_state = 0
        elif position[0] in range(40, 310) and position[1] in range(367, 427):
            if self.game_state == 6:
                self.run_multiple_tests(1000, 0)
                self.game_state = 0
        elif position[0] in range(40, 310) and position[1] in range(430, 490):
            if self.game_state == 6:
                self.run_multiple_tests(1000, 1)
                self.game_state = 0
    
    def mouseMotion(self, buttons, position, rel):
        pass
        
    def draw(self):
        self.screen.blit(self.background_bottom, (348, 101))

        #doors 1 2 3:
        for door in self.doors:
            door.draw(self.screen)
        
        #doors top:
        self.screen.blit(self.background_top, (348, 0))

        self.screen.blit(self.menu, (0, 0))

        if self.game_state == 0:
            self.screen.blit(self.state_0_new, (40, 115))
            self.screen.blit(self.state_0_save, (40, 178))
        elif self.game_state == 1:
            self.screen.blit(self.state_1_1, (40, 115))
            self.screen.blit(self.state_1_2, (40, 178))
            self.screen.blit(self.state_1_3, (40, 241))
        elif self.game_state == 3:
            self.screen.blit(self.state_3_change, (40, 115))
            self.screen.blit(self.state_3_save, (40, 178))
        elif self.game_state == 6:
            self.screen.blit(self.state_0_save, (40, 115))
            self.screen.blit(self.state_0_change, (40, 178))
            self.screen.blit(self.state_0_save, (40, 241))
            self.screen.blit(self.state_0_change, (40, 304))
            self.screen.blit(self.state_0_save, (40, 367))
            self.screen.blit(self.state_0_change, (40, 430))

        self.screen.blit(self.presenter, (980, 215))
        
        if self.game_state == 0:
            self.screen.blit(self.speach_bubble_1, (475, 370))
        elif self.game_state == 1:
            self.screen.blit(self.speach_bubble_2, (475, 370))
        elif self.game_state == 3:
            self.screen.blit(self.speach_bubble_3, (475, 370))
        elif self.game_state == 4:
            if self.winner == 1:
                self.screen.blit(self.speach_bubble_4_win, (475, 370))
            elif self.winner == 2:
                self.screen.blit(self.speach_bubble_4_loose, (475, 370))
        #pygame.draw.rect(self.screen, (255, 0, 0), (40, 241, 270, 60), 1)
        
s = Starter()
s.mainLoop(60)

