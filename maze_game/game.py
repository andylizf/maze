import os
import time

import numpy as np
import re

class Game:
    class DIRECTION:
        LEFT = 'left'
        RIGHT = 'right'
        UP = 'up'
        DOWN = 'down'
        ACTIONS = [LEFT, RIGHT, UP, DOWN]

    def __init__(self, max_row, max_col, worker, treasure, refresh_interval, obstacles=None):
        self.max_row = max_row
        self.max_col = max_col
        self.init_worker = worker.clone()
        self.worker = worker
        self.treasure = treasure
        self.refresh_interval = refresh_interval

        if obstacles:
            for obstacle in obstacles:
                if treasure.equal(obstacle):
                    raise Exception('The treasure point is conflicted with an obstacle point')
            self.obstacles = obstacles
        else:
            self.obstacles = []

    def move(self, action):
        # print(action)

        if action == Game.DIRECTION.LEFT:
            if self.worker.col > 0:
                self.worker.col -= 1
        elif action == Game.DIRECTION.RIGHT:
            if self.worker.col < self.max_col - 1:
                self.worker.col += 1
        elif action == Game.DIRECTION.UP:
            if self.worker.row > 0:
                self.worker.row -= 1
        elif action == Game.DIRECTION.DOWN:
            if self.worker.row < self.max_row - 1:
                self.worker.row += 1
        else:
            raise Exception('Not supported action: {}'.format(action))

        return self.feedback()

    def feedback(self):
        state = self.worker.toString()
        reward = 0
        if self.worker.equal(self.treasure):
            reward = 1
        for obstacle in self.obstacles:
            if self.worker.equal(obstacle):
                reward = -1
        return state, reward

    def reset(self):
        self.worker = self.init_worker.clone()
        return self.worker.toString()

    def display(self):
        os.system('cls')
        arr = np.zeros((self.max_row, self.max_col))
        arr[self.treasure.row][self.treasure.col] = 8
        arr[self.worker.row][self.worker.col] = 1
        for obstacle in self.obstacles:
            arr[obstacle.row][obstacle.col] = 4
        for i in arr:
            print(i)
        time.sleep(self.refresh_interval)


class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def equal(self, other_point):
        return self.row == other_point.row and self.col == other_point.col

    def toString(self):
        return "({},{})".format(str(self.row), str(self.col))

    def clone(self):
        return Point(self.row, self.col)

def toPoint(str):
    pattern = re.compile(r'\((?P<x>\d), ?(?P<y>\d)\)')
    match = pattern.match(str)
    if match:
        (x, y) = match.group('x', 'y')
        return Point(int(x), int(y))
    else:
        return False

refresh_interval = 0.05  # 该参数用于定时显示迷宫情况
def startGame():
    print('Press ^C at any time to quit.')
    max_row = input("max_row: [4] ")
    max_row = max_row if isinstance(max_row, int) else 4
    
    max_col = input("col: [4] ")
    max_col = max_col if isinstance(max_col, int) else 4

    worker = toPoint(input("woker position: [(0, 0)] "))
    worker = Point(0, 0) if not worker else worker

    treasure = toPoint(input("treasure position: [(2, 2)] "))
    treasure = Point(2, 2) if not treasure else treasure

    obstacles = input("obstacles position: [(1, 2) (2, 1)] ").split()
    obstacles = [toPoint(x) for x in obstacles]
    obstacles = list(set(obstacles))
    if False in obstacles or len(obstacles) == 0:
        obstacles = [
            Point(1, 2),
            Point(2, 1),
        ]

    os.system('cls')
    print("max_row:", max_row)
    print("max_col:", max_col)
    print("woker position:", worker.toString())
    print("treasure position:", treasure.toString())
    print("obstacles position:", [x.toString() for x in obstacles])

    return Game(
        max_row=max_row,
        max_col=max_col,
        worker=worker,
        treasure=treasure,
        obstacles=obstacles,
        refresh_interval=refresh_interval
    )