from maze_game.game import Game, Point
from agent import QLearningAgent
import re
import os

"""
使用强化学习走迷宫,由于刚开始的状态是随机的,所以当迷宫面积较大的时候,可能会导致训练时间太长,可以尝试利用 A* 算法原理,
帮助更快找到treasure
迷宫展示字典:
    1: worker
    4: obstacle
    8: treasure
reward字典:
    -1: obstacle
     1: treasure
经测试,跑完 30 个 episode,约耗时 30s
"""

def toPoint(str):
    pattern = re.compile(r'\((?P<x>\d), ?(?P<y>\d)\)')
    match = pattern.match(str)
    if match:
        (x, y) = match.group('x', 'y')
        return Point(int(x), int(y))
    else:
        return False


if __name__ == '__main__':
    refresh_interval = 0.05  # 该参数用于定时显示迷宫情况

    episode = 30  # 训练多少回合

    epsilon = 0.8  # 使用历史经验的概率, 若值为0.9,则有 90% 的情况下,会根据历史经验选择 action, 10% 的情况下,随机选择 action
    learning_rate = 0.01  # 根据公式可知,该值越大,则旧训练数据被保留的就越少
    discount_factor = 0.9  #

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
    key = input('Do you want to see the training process? [y] ')
    key = key == 'y' or key == ''

    env = Game(
        max_row=max_row,
        max_col=max_col,
        worker=worker,
        treasure=treasure,
        obstacles=obstacles,
        refresh_interval=refresh_interval
    )
    agent = QLearningAgent(
        epsilon=epsilon,
        learning_rate=learning_rate,
        discount_factor=discount_factor,
        actions=Game.DIRECTION.ACTIONS
    )
    successful_step_counter_arr = []
    failed_step_counter_arr = []

    if key:
        env.display()

    for eps in range(1, episode + 1):

        cur_state = env.reset()
        step_counter = 0

        while True:
            step_counter += 1

            if key:
                env.display()

            action = agent.choose_action(cur_state)

            next_state, reward = env.move(action)

            agent.learn(
                cur_state=cur_state,
                action=action,
                reward=reward,
                next_state=next_state
            )

            cur_state = next_state

            if reward != 0:
                break

        if reward > 0:
            successful_step_counter_arr.append(step_counter)
        elif reward < 0:
            failed_step_counter_arr.append(step_counter)

        if key:
            print(
                'total episode: {}\n'
                'current episode: {}\n'
                'reward: {}\nsteps: {}\n'
                'successful steps record: {}\n'
                'failed steps record: {}'
                    .format(
                    episode,
                    eps,
                    reward,
                    step_counter,
                    successful_step_counter_arr,
                    failed_step_counter_arr
                )
            )
            input('press enter to next episode...')

        # print(agent.q_table)
        # print('successful steps record: {}'.format(succeed_step_counter_arr))

    if not key:
        print(
            'total episode: {}\n'
            'current episode: {}\n'
            'reward: {}\nsteps: {}\n'
            'successful steps record: {}\n'
            'failed steps record: {}'
                .format(
                episode,
                eps,
                reward,
                step_counter,
                successful_step_counter_arr,
                failed_step_counter_arr
            )
        )