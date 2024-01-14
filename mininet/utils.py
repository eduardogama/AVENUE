import numpy as np
import random 
import math


def next_time(rateParameter: float, RAND_MAX: int = 0):
    return -math.log(1.0 - random.random() / (RAND_MAX + 1)) / rateParameter

def zipf_distribution(n, alpha):
    # Generate Zipf distribution
    dist = [1.0 / (i ** alpha) for i in range(1, n + 1)]
    dist = [x / sum(dist) for x in dist]
    return dist

def zipf_selection(data, alpha, num_samples):
    n = len(data)
    zipf_dist = zipf_distribution(n, alpha)
    selected_indices = np.random.choice(n, num_samples, p=zipf_dist)
    selected_elements = [data[i] for i in selected_indices]
    return selected_elements