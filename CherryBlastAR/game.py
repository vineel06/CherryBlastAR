import random
from balloon import Balloon
from particles import ParticleSystem

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
        self.speed_level = 1
        self.balloons = []
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_interval = 30
        self.particles = ParticleSystem()

    def update(self):
        if self.game_over:
            return
        for b in self.balloons:
            b.move()
        self.balloons = [b for b in self.balloons if not b.is_offscreen(self.height)]
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_balloon()
            self.spawn_timer = 0
        self.particles.update()

    def spawn_balloon(self):
        bomb = random.random() < 0.1
        self.balloons.append(Balloon(self.width, self.height, self.speed_level, bomb))

    def shoot(self, shoot_pos):
        for i, b in enumerate(self.balloons):
            if b.is_shot(shoot_pos):
                if b.bomb:
                    self.game_over = True
                    return True, True
                else:
                    self.balloons.pop(i)
                    self.score += 1
                    self.particles.add_explosion(shoot_pos[0], shoot_pos[1], (0,0,255))
                    if self.score % 5 == 0:
                        self.speed_level += 1
                        for bal in self.balloons:
                            bal.speed = self.speed_level
                    return False, True
        return False, False

    def draw_balloons(self, frame):
        for b in self.balloons:
            b.draw(frame)

    def draw_particles(self, frame):
        self.particles.draw(frame)