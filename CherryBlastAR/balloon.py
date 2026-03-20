import random
import cv2
import numpy as np

class Balloon:
    COLORS = [
        (0, 0, 255),    # red
        (0, 255, 0),    # green
        (255, 0, 0),    # blue
        (0, 255, 255),  # yellow
        (255, 0, 255),  # magenta
        (255, 255, 0)   # cyan
    ]

    def __init__(self, width, height, speed=1, bomb=False):
        self.x = random.randint(50, width - 50)
        self.y = height - 50
        self.speed = speed
        self.radius = 30
        self.bomb = bomb
        if bomb:
            self.color = (0, 0, 0)
        else:
            self.color = random.choice(self.COLORS)
        self.glow_color = tuple(c + 50 if c + 50 <= 255 else 255 for c in self.color)

    def move(self):
        self.y -= self.speed

    def draw(self, frame):
        # Glow effect
        overlay = frame.copy()
        cv2.circle(overlay, (self.x, self.y), self.radius + 5, self.glow_color, -1)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        # Main balloon
        cv2.circle(frame, (self.x, self.y), self.radius, self.color, -1)
        # String
        cv2.line(frame, (self.x, self.y + self.radius), (self.x, self.y + self.radius + 20), (255, 255, 255), 2)
        # Bomb text
        if self.bomb:
            cv2.putText(frame, "BOMB", (self.x-20, self.y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        else:
            # Small highlight
            cv2.circle(frame, (self.x-8, self.y-8), 5, (255,255,255), -1)

    def is_shot(self, shoot_pos):
        dist = np.linalg.norm(np.array([self.x, self.y]) - np.array(shoot_pos))
        return dist < self.radius

    def is_offscreen(self, height):
        return self.y + self.radius < 0