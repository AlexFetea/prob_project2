prev_random = 1000


def get_next_random():
    global prev_random
    prev_random = ((24693 * prev_random + 3517) % (2 ** 17))
    return prev_random / (2**17)


for i in range(1, 54):
    u = get_next_random()
    if i >= 51:
        print(f"i: {i}, u_i: {u}")