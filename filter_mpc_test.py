import time

import numpy as np
from scipy import signal
from scipy.optimize import minimize

numerator = [0, 0.02643]  # Example coefficients, replace with your own
denominator = [1, -0.9714]  # Example coefficients, replace with your own
def system_model2(y, u_sequence):
    return np.concatenate((np.array([y]), np.array(y + signal.lfilter(numerator, denominator, u_sequence[0:len(u_sequence)-1]))))

q = 1000.0  # State deviation weight
r = 0.0001  # Control effort weight
def cost_function2(u_sequence, y, setpoint_sequence):
    y_predicted = system_model2(y, u_sequence)
    print("y_pred =", y_predicted, "u_sequence =", u_sequence)
    return np.sum(q * (setpoint_sequence - y_predicted)**2 + r * u_sequence**2)


u_min = 0.0
u_max = 4.0
def mpc_controller2(y, set_point, u, horizon):

    # Define bounds for control inputs
    bounds = [(u_min, u_max)] * horizon
    setpoint_sequence = np.full(horizon, set_point)
    u_sequence_initial = np.full(horizon, u)

    # Define optimization problem
    optimization_result = minimize(
        cost_function2,
        u_sequence_initial,
        args=(y, setpoint_sequence),
        bounds=bounds,
        method='SLSQP',
        options={'maxiter': 5}
    )

    # Extract optimal control sequence
    u_sequence_optimal = optimization_result.x

    # Return next optimal control input
    return u_sequence_optimal[0]


def system_model(y, u):
    delta_y = (-1 / T) * y + (K / T) * u
    y += delta_y * H
    return y


def system_model1(y, u):
    global next
    y = next
    delta_y = (-1 / T) * y + (K / T) * u
    next += delta_y * H
    return y

horizon = 5
process_variable = 0
set_point = 2
control_variable = 0
next = process_variable

K = 0.925156  # Gain
T = 3.45  # Time constant
T0 = 0.1  # Dead time
H = 0.1  # Sampling time

for i in range(200):
    control_variable = mpc_controller2(process_variable, set_point, control_variable, horizon)
    process_variable = system_model1(process_variable, control_variable)
    print("y =", process_variable, " cv =", control_variable)

