curr_random = 1000


def get_next_random():
    global curr_random
    curr_random = (24693 * curr_random + 3517) % (2 ** 17)
    return curr_random


for i in range(1, 54):
    get_next_random()
    if i >= 51:
        print(f"i: {i}, u_i: {curr_random}")