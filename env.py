#! /usr/bin/env python3

import random

class Easy21:
    def __init__(self):
        self.dealerValue = 0

    def reset(self):
        self.dealerValue = random.randint(1, 10)
        return random.randint(1, 10), self.dealerValue

    def step(self, present_state, action):
        next_state, reward = None, None
        player, dealer = present_state
        reward = 0
        terminal = False

        # Player chooses to hit.
        if action == "hit":
            value = self.draw()
            player += value

            if not 1 <= player <= 21:
                reward = -1
                terminal = True
            else:
                reward = 0
                terminal = False

        # Player chooses to stick. Dealer takes the turn.
        elif action == "stick":
            terminal = True

            while 0 < self.dealerValue < 17:
                self.dealerValue += self.draw()

            # Check if dealer went bust.
            if not 1 <= self.dealerValue <= 21:
                reward = 1

            # Check who has larger sum.
            if player > self.dealerValue:
                reward = 1
            elif self.dealerValue > player:
                reward = -1
            else:
                reward = 0

        return (player, dealer), reward, terminal

    def draw(self):
        value = random.randint(1, 10)
        if random.random() < 1/3:
            return -value
        else:
            return value

    def get_actions(self):
        return ["hit", "stick"]

if __name__ == "__main__":
    random.seed(0)

    for i in range(10):
        g = Easy21()
        state = (g.draw(), g.draw())
        action = None

        if i % 2 == 0:
            action = "hit"
        else:
            action = "stick"

        _, r = g.step(state, action)

        print(f"{i + 1}\t=> action: {action}, reward: {r}")