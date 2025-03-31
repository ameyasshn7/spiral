import cython
import sympy
import numpy as np 
import matplotlib.pyplot as plt
import math

FS=(12,12)



def is_prime(n: int) -> bool:
    if n <= 1 and n < 0:
        raise ValueError("Only Positive integers")
    if n < 3:
        return False
    if n  % 2 == 0 or n % 3 == 0 or n < 3:
        return False
    

    upper_bound =int((n **  0.5))
    d = 5

    while d < upper_bound:
        if n % d == 0 or n % d + 2 == 0:
            return False
        d += 6
    
    return True



def generate_ulam_spiral(size: int):
    num = 1
    step_size = 1
    x = size // 2
    y = size // 2
    
    if np.mod(size, 2) == 0:
        raise ValueError("Size can not be even")
    
    
    # Fix: zeros, not zeroes
    grid = np.zeros((size,size), dtype=np.uint8)
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    direction = 0
    while num <= int(size ** 2):
        for _ in range(2):
            for _ in range(step_size):
                if 0 <= x < size and 0 <= y < size:
                    if is_prime(num):
                        grid[size - y - 1, x] = 1
                
                x += directions[direction][0]
                y += directions[direction][1]
                num += 1

                if num > (size ** 2):
                    break
            
            direction = np.mod(direction + 1, 4)
        step_size += 1
    return grid

def compute_grid_size(n=100):

    size = int(np.ceil(np.sqrt(n)))
    if np.mod(size,2) == 0:
        size += 1
    
    return size


def plot_ulam_spiral(size=None, n=None, figsize=(8, 8), cmap="plasma", grid_color="white", point_color="white"):

    if size is None and n is not None:
        size = compute_grid_size(n)
    elif size is None and n is None:
        raise ValueError("Both size and n are None")
    elif size is not None and n is not None:
        raise ValueError("Both size and n are given")

    spiral = generate_ulam_spiral(size)
    plt.figure(figsize=figsize)
    plt.imshow(spiral, cmap=cmap, interpolation="nearest")
    plt.gca().set_aspect("equal")
    plt.gca().set_facecolor(grid_color)
    
    # Add gridlines for aesthetics
    plt.grid(visible=True, color=grid_color, linestyle='-', linewidth=0.5)
    plt.xticks([])
    plt.yticks([])
    
    # Highlight prime points
    plt.imshow(spiral, cmap=cmap, interpolation="nearest")
    plt.gca().set_facecolor(grid_color)
    plt.axis("off")



if __name__ == '__main__':
    plot_ulam_spiral(n=10000, figsize=(100,100))
    plt.savefig("ulam_spiral_3.jpg", dpi=300, bbox_inches="tight", format="jpg")    
    
    
    