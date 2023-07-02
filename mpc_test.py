import numpy as np
from scipy.optimize import minimize

K = 0.925156  # Gain
T = 3.45  # Time constant
T0 = 0.1  # Dead time
H = 0.1  # Sampling time
Q = 1.0  # State deviation weight
R = 0.1  # Control effort weight
u_min = 0.0
u_max = 4.0


# MY MPC
next = 0.0
def system_model(y, u):
    global next
    y = next
    delta_y = (-1 / T) * y + (K / T) * u
    next = next + delta_y * H
    # print(f"u = {u} y = {y}")
    return y


def system_model_approx(y, u):

    y = (K * np.exp(-T0 / H) * u) / (H + H - H * np.exp(-T0 / H))
    return y

def fopdt_model(y, u):
    return K * (1 - np.exp(-H/T)) * np.exp(-y/T) + u

y = 0.0
y0 = 0.0
u = 2.0
for i in range(300):
    y = system_model(y, u)
    # y0 = system_model_approx(y0, 2)
    y0 = fopdt_model(y0, u)
    print(f"y = {y}, y_approx = {y0}")


# def cost_function(u_sequence, y, setpoint_sequence):
#     global next
#     cost = 0.0
#     next = y
#     for sp, u in zip(setpoint_sequence, u_sequence):
#         y_predicted = system_model(y, u)
#         cost += Q * (y_predicted - sp)**2 + R * u**2
#         y = y_predicted
#     return cost

# def mpc_controller(y, setpoint_sequence, u, horizon):

#     # Define bounds for control inputs
#     bounds = [(u_min, u_max)] * horizon

#     # Set initial control sequence
#     u_sequence_initial = [u] * horizon

#     # Define optimization problem
#     optimization_result = minimize(
#         cost_function,
#         u_sequence_initial,
#         args=(y, setpoint_sequence),
#         bounds=bounds,
#         method='SLSQP'
#     )

#     # Extract optimal control sequence
#     u_sequence_optimal = optimization_result.x
#     print(u_sequence_optimal)
#     # Return next optimal control input
#     return u_sequence_optimal[0]

# horizon = 10
# print("AUEUEUEUE")
# print(mpc_controller(0, [1] * horizon, 0, horizon))