import pygame
import sys
import time

from settings import *
from sprites import BG, Ground, Plane, Obstacle


class Game:
    def __init__(self):
        # setup
        self.score_rect = None
        self.score_surf = None
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load('../graphics/environmennt/background.png').get_height()
        self.scale_factor = window_height / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, scale_factor=1)
        self.obstacle = Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor)

        # timer
        self.obstacle_timer = 0
        pygame.time.set_timer(self.obstacle_timer, 1200)

        # text
        self.font = pygame.font.Font('../graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        # counter obstacles
        self.number_obstacles = 0
        self.last_score = 0

        # menu
        self.menu_surf = pygame.image.load('../graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center=(window_width / 2, window_height / 2))

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) \
                or self.plane.rect.top <= 0:

            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()

            self.active = False
            self.plane.kill()

    def display_score(self):
        if self.active:
            if self.number_obstacles >= 0:
                self.score = self.number_obstacles
            self.score_surf = self.font.render(str(self.score), True, 'black')
            self.score_rect = self.score_surf.get_rect(midtop=(window_width / 2, window_height / 10))
            self.display_surface.blit(self.score_surf, self.score_rect)
            if self.last_score <= self.score:
                self.last_score = self.score

        else:
            last_score_surf = self.font.render(str(self.last_score), True, 'black')
            last_score_rect = last_score_surf.get_rect(midtop=(window_width / 2, (window_height / 10) * 6))
            self.display_surface.blit(self.score_surf, self.score_rect)
            self.display_surface.blit(last_score_surf, last_score_rect)
            self.number_obstacles = -1

    def run(self):
        last_time = time.time()
        while True:
            # delta time
            dt = time.time() - last_time
            # attention! if miss this, the background image speed inscrease forever
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.active:
                            self.plane.jump()

                        else:
                            self.plane = Plane(self.all_sprites, scale_factor=1)
                            self.plane.jump()
                            self.active = True

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == 0 and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor)
                    if self.plane.pos.x > self.obstacle.pos.x:
                        self.number_obstacles += 1

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
