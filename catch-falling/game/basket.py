"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Normal movement speed
        self.speed = speed
        self.normal_speed = speed

        # Speed boost settings
        self.boost_speed = speed * 2
        self.boosted_frames = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )

    def activate_boost(self, duration=180):
        """
        Activate the temporary speed boost.
        """
        self.boosted_frames = duration
        self.speed = self.boost_speed

    def update_boost(self):
        """
        Update the speed boost timer.
        Return to normal speed when the boost expires.
        """
        if self.boosted_frames > 0:
            self.boosted_frames -= 1

            if self.boosted_frames <= 0:
                self.speed = self.normal_speed

    def is_boosted(self):
        """
        Return True while the speed boost is active.
        """
        return self.boosted_frames > 0
