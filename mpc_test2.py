import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


def fopdt_model(y, u, T, L, K):
    return K * (1 - np.exp(-L/T)) * np.exp(-y/T) + u

def objective(u, y_setpoint, y0, T, L, K, N):
    y_pred = np.zeros(N+1)
    y_pred[0] = y0
    for i in range(N):
        y_pred[i+1] = fopdt_model(y_pred[i], u[i], T, L, K)
    return np.sum(3.0 * (y_pred[:-1] - y_setpoint)**2)

def mpc_controller(y_setpoint, y0, T, L, K, N, umin, umax):
    u_init = np.zeros(N)
    bounds = [(umin, umax) for _ in range(N)]
    result = minimize(objective, u_init, args=(y_setpoint, y0, T, L, K, N), bounds=bounds)
    return result.x[0]

# Example usage
y_setpoint = 3.0  # Desired setpoint
y0 = 2.8  # Initial output value
T = 3.45  # Time constant
L = 0.1  # Time delay
K = 0.925156  # Gain
N = 10  # Horizon length
umin = 0.0  # Minimum control signal
umax = 4.0  # Maximum control signal

# Call the MPC controller
u = mpc_controller(y_setpoint, y0, T, L, K, N, umin, umax)
print("Control signal:", u)
