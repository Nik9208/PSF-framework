import numpy as np

def generate_constant(n=1000, value=1.0):
    return np.full(n, value)

def generate_gaussian_white_noise(n=1000, seed=None):
    if seed is not None: np.random.seed(seed)
    return np.random.normal(0, 1, n)

def generate_uniform_noise(n=1000, seed=None):
    if seed is not None: np.random.seed(seed)
    return np.random.uniform(-1, 1, n)

def generate_pink_noise(n=1000, seed=None):
    if seed is not None: np.random.seed(seed)
    # Simple 1/f noise generator via IFFT
    f = np.fft.rfftfreq(n)
    f[0] = 1.0  # avoid divide by zero
    s_scale = 1.0 / np.sqrt(f)
    s_scale[0] = 0.0
    awgn = np.fft.rfft(np.random.normal(0, 1, n))
    pink = np.fft.irfft(awgn * s_scale, n=n)
    # normalize
    pink = (pink - np.mean(pink)) / np.std(pink)
    return pink

def generate_sine(n=1000, freq=0.01):
    t = np.arange(n)
    return np.sin(2 * np.pi * freq * t)

def generate_sine_trend(n=1000, freq=0.01, slope=0.005):
    t = np.arange(n)
    return np.sin(2 * np.pi * freq * t) + slope * t

def generate_ar1(n=1000, phi=0.8, seed=None):
    if seed is not None: np.random.seed(seed)
    noise = np.random.normal(0, 1, n)
def generate_ar1(n=1000, phi=0.5, seed=None):
    """Generates an AR(1) process with coefficient phi."""
    if seed is not None:
        np.random.seed(seed)
    x = np.zeros(n)
    w = np.random.normal(0, 1, n)
    x[0] = w[0]
    for i in range(1, n):
        x[i] = phi * x[i-1] + w[i]
    return x

def generate_lorenz(n=1000, dt=0.01, sigma=10.0, rho=28.0, beta=8.0/3.0, seed=None):
    """Generates x-coordinate of the Lorenz attractor."""
    if seed is not None:
        np.random.seed(seed)
    # transient
    t_trans = 1000
    x, y, z = 1.0, 1.0, 1.0
    for _ in range(t_trans):
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x, y, z = x + dx, y + dy, z + dz

    xs = []
    for _ in range(n):
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x, y, z = x + dx, y + dy, z + dz
        xs.append(x)
    return np.array(xs)

def generate_changepoint(n=1000, change_idx=None, seed=None):
    if seed is not None: np.random.seed(seed)
    if change_idx is None:
        change_idx = n // 2
    # Variance shift
    part1 = np.random.normal(0, 1, change_idx)
    part2 = np.random.normal(0, 5, n - change_idx)
    return np.concatenate([part1, part2])
