import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import argparse

# Mandelbrot set calculation
def mandelbrot(c, max_iter=100):
    z = complex(0, 0)
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return i
    return max_iter

def mandelbrot_set(width, height, x_min=-2, x_max=1, y_min=-1, y_max=1, max_iter=100):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    m = np.zeros((width, height))
    
    for i in range(width):
        for j in range(height):
            c = complex(x[i], y[j])
            m[i, j] = mandelbrot(c, max_iter)
    
    return m.T  # Transpose for correct orientation

# Julia set calculation
def julia_set(width, height, c=complex(-0.7, 0.27), x_min=-1.5, x_max=1.5, 
              y_min=-1.5, y_max=1.5, max_iter=100):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    j = np.zeros((width, height))
    
    for i in range(width):
        for j_idx in range(height):
            z = complex(x[i], y[j_idx])
            iteration = 0
            
            while abs(z) <= 2 and iteration < max_iter:
                z = z*z + c
                iteration += 1
            
            j[i, j_idx] = iteration
    
    return j.T  # Transpose for correct orientation

# Newton fractal
def newton_fractal(width, height, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5, max_iter=20):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    n = np.zeros((width, height), dtype=np.int32)
    
    # Roots of p(z) = z³ - 1
    roots = [complex(1, 0), complex(-0.5, np.sqrt(3)/2), complex(-0.5, -np.sqrt(3)/2)]
    
    for i in range(width):
        for j in range(height):
            z = complex(x[i], y[j])
            
            for iteration in range(max_iter):
                # f(z) = z³ - 1, f'(z) = 3z²
                z_next = z - (z**3 - 1) / (3 * z**2)
                if abs(z_next - z) < 1e-6:
                    # Found a root, determine which one
                    for k, root in enumerate(roots):
                        if abs(z_next - root) < 1e-3:
                            n[i, j] = k + 1
                            break
                    break
                z = z_next
    
    return n.T

# Sierpinski carpet
def sierpinski_carpet(width, height, iterations=6):
    carpet = np.ones((width, height))
    
    def cut_square(x_min, y_min, size):
        if size < 1:
            return
        
        # Cut out middle square
        x_mid = x_min + size // 3
        y_mid = y_min + size // 3
        carpet[x_mid:x_mid + size//3, y_mid:y_mid + size//3] = 0
        
        # Recursive calls for the 8 remaining squares
        new_size = size // 3
        for i in range(3):
            for j in range(3):
                if not (i == 1 and j == 1):  # Skip the middle square
                    cut_square(x_min + i * new_size, y_min + j * new_size, new_size)
    
    size = min(width, height)
    start_x = (width - size) // 2
    start_y = (height - size) // 2
    cut_square(start_x, start_y, size)
    
    return carpet

# Custom color maps
def create_colormap(name):
    if name == "fire":
        colors = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]
        return LinearSegmentedColormap.from_list("fire", colors)
    elif name == "ocean":
        colors = [(0, 0, 0.5), (0, 0, 1), (0, 1, 1), (1, 1, 1)]
        return LinearSegmentedColormap.from_list("ocean", colors)
    elif name == "forest":
        colors = [(0, 0, 0), (0, 0.5, 0), (0, 1, 0), (1, 1, 0)]
        return LinearSegmentedColormap.from_list("forest", colors)
    else:
        return plt.get_cmap(name)

def save_fractal(fractal, filename, cmap="magma"):
    plt.figure(figsize=(10, 10))
    plt.imshow(fractal, cmap=create_colormap(cmap))
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Generate various fractals")
    parser.add_argument("--type", default="mandelbrot", choices=["mandelbrot", "julia", "newton", "sierpinski"],
                        help="Type of fractal to generate")
    parser.add_argument("--width", type=int, default=800, help="Image width in pixels")
    parser.add_argument("--height", type=int, default=800, help="Image height in pixels")
    parser.add_argument("--cmap", default="magma", help="Colormap to use (matplotlib name or custom: fire, ocean, forest)")
    parser.add_argument("--iterations", type=int, default=100, help="Maximum iterations")
    parser.add_argument("--output", default="fractal.png", help="Output filename")
    args = parser.parse_args()
    
    width, height = args.width, args.height
    
    if args.type == "mandelbrot":
        fractal = mandelbrot_set(width, height, max_iter=args.iterations)
    elif args.type == "julia":
        fractal = julia_set(width, height, max_iter=args.iterations)
    elif args.type == "newton":
        fractal = newton_fractal(width, height, max_iter=args.iterations)
    elif args.type == "sierpinski":
        fractal = sierpinski_carpet(width, height, iterations=min(8, args.iterations))
    
    save_fractal(fractal, args.output, args.cmap)
    print(f"Fractal saved to {args.output}")

if __name__ == "__main__":
    main()