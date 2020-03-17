#! /usr/bin/env python3

import random

class Easy21:
    def __init__(self):
        self.colour = ["B", "B", "R"]

    def step(self, present_state, action):
        next_state, reward = None, None
        player, dealer = present_state

        # First move of the game.
        if player == 0 and dealer == 0:
            player = self.draw()
            dealer = self.draw()
        # Player chooses to hit.
        elif action == "hit":
            red_or_black = random.choice(self.colour)
            value = self.draw()

            # Subtract for red cards
            if red_or_black == "R":
                player -= value
            # Add for black cards
            else:
                player += value

        # Player chooses to stick. Dealer takes the turn.
        elif action == "stick":
            if dealer < 17:
                red_or_black = random.choice(self.colour)
                value = self.draw()

                # Subtract for red cards
                if red_or_black == "R":
                    player -= value
                # Add for black cards
                else:
                    player += value

        # Check who has larger sum.
        if player > dealer:
            reward = 1
        elif dealer > player:
            reward = -1
        else:
            reward = 0

        # Check if player went bust.
        if player > 21 or player < 1:
            reward = -1
        # Check if dealer went bust.
        if dealer > 21 or dealer < 1:
            reward = 1

        next_state = (player, dealer)

        return next_state, reward

    def draw(self):
        return random.randint(1, 10)

if __name__ == "__main__":
    random.seed(0)

    g = Easy21()
    state = (0, 0)

    for i in range(10):
        if i % 2 == 0:
            state, r = g.step(state, "hit")
        else:
            state, r = g.step(state, "stick")

        print(f"state: {state}, reward: {r}")