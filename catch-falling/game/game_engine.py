"""
GameEngine: owns the basket and all falling objects.

Tasks completed:
- Task 1: Fixed falling-object collision detection and list mutation.
- Task 2: Improved basket boundary handling.
- Task 3: Controlled object spawning.
- Task 4: Temporary basket speed boost.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT


SPAWN_INTERVAL_FRAMES = 50
MAX_MISSES = 5


# ============================================================
# TASK 3 - Controlled Object Spawning
# ============================================================

MIN_SPAWN_INTERVAL = 25
MAX_SPAWN_INTERVAL = 65

MAX_OBJECTS = 5

MIN_SPAWN_DISTANCE = 80


# ============================================================
# TASK 4 - Temporary Speed Boost
# ============================================================

BOOST_DURATION = 180


class GameEngine:

    def __init__(self):

        self.basket = Basket(
            x=WIDTH / 2,
            y=HEIGHT - 30
        )

        self.objects = []

        self.frames_until_spawn = 0

        self.score = 0

        self.misses = 0

        self.game_over = False

        # Task 3:
        # Remember the previous spawn position.
        self.last_spawn_x = None


    # ========================================================
    # TASK 3 - Controlled Object Spawning
    # ========================================================

    def _spawn_object(self):

        # Do not create more objects than the allowed limit.
        if len(self.objects) >= MAX_OBJECTS:
            return

        # Keep objects inside the playable horizontal area.
        min_x = 20
        max_x = WIDTH - 20

        x = random.randint(
            min_x,
            max_x
        )

        # Avoid repeatedly spawning at almost the same location.
        if self.last_spawn_x is not None:

            for _ in range(10):

                candidate = random.randint(
                    min_x,
                    max_x
                )

                if abs(
                    candidate - self.last_spawn_x
                ) >= MIN_SPAWN_DISTANCE:

                    x = candidate
                    break

        self.last_spawn_x = x

        self.objects.append(
            FallingObject(
                x=x,
                y=-14,
                speed=3
            )
        )


    # ========================================================
    # TASK 2 - Basket Control
    # ========================================================

    def handle_input(self, keys_pressed):

        if self.game_over:
            return

        # Continuous left movement.
        if keys_pressed[pygame.K_LEFT]:

            self.basket.x -= self.basket.speed

        # Continuous right movement.
        if keys_pressed[pygame.K_RIGHT]:

            self.basket.x += self.basket.speed

        # Keep the COMPLETE basket inside the screen.
        #
        # basket.x represents the center of the basket.
        half_width = self.basket.width / 2

        self.basket.x = max(
            half_width,
            min(
                WIDTH - half_width,
                self.basket.x
            )
        )


    # ========================================================
    # KEYBOARD EVENTS
    # ========================================================

    def handle_keydown(self, key):

        # Restart after game over.
        if self.game_over and key == pygame.K_r:

            self.__init__()

        # Task 4:
        # SPACE activates the temporary speed boost.
        if not self.game_over and key == pygame.K_SPACE:

            self.basket.activate_boost(
                BOOST_DURATION
            )


    # ========================================================
    # UPDATE GAME
    # ========================================================

    def update(self):

        if self.game_over:
            return


        # ====================================================
        # TASK 4 - Update speed boost
        # ====================================================

        self.basket.update_boost()


        # ====================================================
        # TASK 3 - Spawn objects
        # ====================================================

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:

            if len(self.objects) < MAX_OBJECTS:

                self._spawn_object()

            # Random spawning interval.
            self.frames_until_spawn = random.randint(
                MIN_SPAWN_INTERVAL,
                MAX_SPAWN_INTERVAL
            )


        # ====================================================
        # Update falling objects
        # ====================================================

        for obj in self.objects:

            obj.update()


        # ====================================================
        # TASK 1 - Collision detection
        # ====================================================

        basket_rect = self.basket.get_rect()

        caught_objects = []

        for obj in self.objects:

            if is_caught(
                basket_rect,
                obj
            ):

                self.score += 1

                caught_objects.append(obj)


        # Remove caught objects AFTER iteration.
        #
        # This prevents the list mutation bug.
        for obj in caught_objects:

            self.objects.remove(obj)


        # ====================================================
        # Missed objects
        # ====================================================

        missed = [
            o
            for o in self.objects
            if o.is_past_bottom(HEIGHT)
        ]


        if missed:

            self.objects = [
                o
                for o in self.objects
                if not o.is_past_bottom(HEIGHT)
            ]

            self.misses += len(missed)


            if self.misses >= MAX_MISSES:

                self.game_over = True


    # ========================================================
    # DRAW
    # ========================================================

    def draw(
        self,
        surface,
        font
    ):

        from game import renderer


        renderer.draw_scene(
            surface,
            self.basket,
            self.objects
        )


        # Score
        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )


        # Misses
        renderer.draw_text(
            surface,
            font,
            f"Misses: {self.misses}/{MAX_MISSES}",
            (10, 36)
        )


        # ====================================================
        # TASK 4 - Speed boost indication
        # ====================================================

        if self.basket.is_boosted():

            seconds_left = (
                self.basket.boosted_frames / 60
            )

            renderer.draw_text(
                surface,
                font,
                f"SPEED BOOST! {seconds_left:.1f}s",
                (10, 62)
            )

        else:

            renderer.draw_text(
                surface,
                font,
                "Press SPACE for Speed Boost",
                (10, 62)
            )


        # ====================================================
        # GAME OVER
        # ====================================================

        if self.game_over:

            renderer.draw_banner(
                surface,
                font,
                (
                    f"Game Over! "
                    f"Final score: {self.score}. "
                    f"Press R to restart."
                )
            )
