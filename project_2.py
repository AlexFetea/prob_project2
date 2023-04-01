import random
import math
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

n = 1000

prev_random = 1000


def get_next_random():
    global prev_random
    prev_random = ((24693 * prev_random + 3517) % (2 ** 17))
    return prev_random / (2**17)

def function_inverse(u):
    if u >= 0 and u <= 1:
        return -12 * math.log(1 - u)
    else:
        raise Exception("u is not in [0,1]")


W_list = []

for game in range(n):
    X = function_inverse(random.uniform(0, 1))
    W = 0
    calls = 0

    while calls < 4:
        calls += 1;
        T = 6  # Turn phone on and dial
        p = random.uniform(0, 1)

        if p <= 0.2:  # event that the line is busy
            T += 3
            T += 1
        elif p <= 0.5:  # event that the customer is unavailable
            T += 25
            T += 1
		elif 0<=X and X<=25:: #event that the customer is available
			T+=X
			T+=1
		else: #event that customer is available but lets phone ring
			T+=25
			T+=1
		W+=T
        if calls >= 4:
            break
    W_list += [W]

series = pd.Series(W_list)
stats = series.describe()
print("Mean:", stats['mean'], "\n")
print("First Quartile:", stats['25%'])
print("Median:", stats['50%'])
print("Third Quartile:", stats['75%'], "\n")

W_less_than_15 = series[series <= 15].count() / n
W_less_than_20 = series[series <= 20].count() / n
W_less_than_30 = series[series <= 30].count() / n
W_less_than_40 = series[series <= 40].count() / n
W_less_than_65 = series[series <= 65].count() / n
W_less_than_85 = series[series <= 85].count() / n
W_less_than_110 = series[series <= 110].count() / n

print("P(W <= 15) =", W_less_than_15)
print("P(W <= 20) =", W_less_than_20)
print("P(W <= 30) =", W_less_than_30)
print("P(W <= 40) =", W_less_than_40)
print("P(W <= 65) =", W_less_than_65)
print("P(W <= 85) =", W_less_than_85)
print("P(W <= 110) =", W_less_than_110)

# Plot of the data points

number_of_bins = 10

bins = np.linspace(min(series), max(series), number_of_bins + 1)

bin_width = (max(series) - min(series)) / number_of_bins
bar_width = bin_width * 0.9

plt.hist(series, bins=bins, edgecolor='black', alpha=0.75, width=bar_width)

xtick_locs = bins[:-1] + (bin_width / 2)
xtick_labels = [f'{round(left, 2)}-{round(right, 2)}' for left, right in zip(bins[:-1], bins[1:])]
plt.xticks(xtick_locs, xtick_labels, rotation=45)

plt.xlabel('W')
plt.ylabel('Frequency')
plt.title('Histogram of Values for W')
plt.show()
