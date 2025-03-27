import numpy as np
import matplotlib.pyplot as plt
import sympy

def get_coordinate(nums):
    # Convert numbers to coordinates in a spiral pattern
    x, y = np.zeros(len(nums)), np.zeros(len(nums))
    for i, num in enumerate(nums):
        # Calculate angle and radius based on number
        angle = np.sqrt(num) * 2 * np.pi
        x[i] = angle * np.cos(angle)
        y[i] = angle * np.sin(angle)
    return x, y

def create_plot(nums, figsize=8, s=None, show_annot=False):
    nums = np.array(list(nums))
    x, y = get_coordinate(nums)
    plt.figure(figsize=(figsize, figsize))
    plt.axis("off")
    plt.scatter(x, y, s=s)
    plt.show()

# Visualize prime numbers
primes = sympy.primerange(0, 20000)
create_plot(primes, s=2)
