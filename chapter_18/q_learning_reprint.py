from __future__ import print_function
import numpy as np
import time
from env import Env
from reprint import output


EPSILON = 0.1
ALPHA = 0.1
GAMMA = 0.9
MAX_STEP = 30

np.random.seed(0)


def epsilon_greedy(Q, state):
    if (np.random.uniform() > 1 - EPSILON) or ((Q[state, :] == 0).all()):
        action = np.random.randint(0, 4)  # 0~3
    else:
        action = Q[state, :].argmax()
    return action


e = Env()
Q = np.zeros((e.state_num, 4))

with output(output_type="list", initial_len=len(e.map), interval=0) as output_list:
    for i in range(100):
        e = Env()
        while (e.is_end is False) and (e.step < MAX_STEP):
            action = epsilon_greedy(Q, e.present_state)
            state = e.present_state
            reward = e.interact(action)
            new_state = e.present_state
            Q[state, action] = (1 - ALPHA) * Q[state, action] + \
                ALPHA * (reward + GAMMA * Q[new_state, :].max())
            e.print_map_with_reprint(output_list)
            time.sleep(0.1)
        for line_num in range(len(e.map)):
            if line_num == 0:
                output_list[0] = 'Episode:{} Total Step:{}, Total Reward:{}'.format(i, e.step, e.total_reward)
            else:
                output_list[line_num] = ''
        time.sleep(2)
