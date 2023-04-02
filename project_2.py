import random
import math
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

n = 1000

random_state = 1000

def get_next_random():
    global random_state
    random_state = (24693 * random_state + 3517) % (2 ** 17)
    return random_state / (2 ** 17)

def function_inverse(u):
    if u >= 0 and u <= 1:
        return -12 * math.log(1 - u)
    else:
        raise Exception("u is not in [0,1]")

def run_trial():
    W = 0

    for call in range(4):
        # Turn phone on and dial
        W += 6

        p = get_next_random()

        if p <= 0.2:
            # Event that the line is busy
            # 3 seconds to detect a busy signal
            W += 3
            # 1 second to end the call
            W += 1
        elif 0.2 <= p <= 0.5:
            # Event that the customer is unavailable
            # 25 seconds to detect that the customer is unavailable
            W += 25
            # 1 second to end the call
            W += 1
        else:
            X = function_inverse(get_next_random())
            # Event that the customer is available
            if 0 <= X <= 25:
                # Customer takes X seconds to answer the call
                W += X
                break
            else:
                # Customer is available but lets phone ring
                # After 25 seconds, the customer hasn't answered, and it
                # takes 1 second to hang up.
                W += 25
                W += 1
    
    return W
    
def plot_stats():
    W_list = [run_trial() for customer in range(n)]

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
    plt.tight_layout()
    plt.show()

def plot_cdf_histogram():
    w = np.array([
        15, 20, 30, 40, 65, 85, 110
    ])
    Fw = np.array([
        0.279, 0.39, 0.496, 0.58, 0.78, 0.895, 0.967
    ])
    plt.title('CDF of W')
    plt.xlabel('W')
    plt.ylabel('F(W)')
    plt.plot(w, Fw, marker='o', linestyle='--', color='b')
    plt.xlim(0, 120)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

    plt.title('1 - F_W(w)')
    plt.xlabel('W')
    plt.ylabel('1 - F_W(W)')
    plt.plot(w, 1 - Fw, marker='o', linestyle='--', color='b')
    plt.xlim(0, 120)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

    # Calculate linear regression
    import scipy.stats as stats

    result = stats.linregress(w, np.log(1 - Fw))
    slope = result.slope
    intercept = result.intercept
    rvalue = result.rvalue
    pvalue = result.pvalue
    stderr = result.stderr
    intercept_stderr = result.intercept_stderr
    print("Slope:", slope)
    print("Intercept:", intercept)
    print("R^2:", rvalue ** 2)
    print("p:", pvalue)
    print("Standard Error:", stderr)
    print("Intercept Standard Error:", intercept_stderr)
    print("lambda:", -1 / slope)

    # plot with result
    plt.title("CDF of W")
    plt.xlabel("W")
    plt.ylabel("F_W(W)")
    # label for legend
    linsp = np.linspace(0, 120, 100)
    plt.plot(linsp, 1 - np.exp(slope * linsp + intercept), linestyle='-', color='r', label=f'Regression: 1 - e^({slope:.3f} * W + {intercept:.3f})')
    plt.plot(w, Fw, marker='o', linestyle='--', color='b', label='Raw data')
    plt.legend()
    plt.show()

plot_cdf_histogram()
