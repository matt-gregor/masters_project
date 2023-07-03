import profile

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

# System parameters
K = 0.925156  # Gain
T = 3.45  # Time constant
T0 = 0.1  # Dead time
H = 0.1  # Sampling time
# Cost function parameters
Q = 4.1  # State deviation weight
R = 0.1  # Control effort weight
# Control input constraints
u_min = 0.0
u_max = 4.0
bruh = 1.25

def system_model(y, u):
    delta_y = (-1 / T) * y + (K / T) * u
    y += delta_y * H
    return y


def cost_function(u_sequence, y, setpoint_sequence):
    global y_prev_mpc
    cost = 0.0
    y_prev_mpc = y
    for sp, u in zip(setpoint_sequence, u_sequence):
        y_predicted = system_model(y, u)
        cost += Q * (sp - y_predicted)**2 + R * u**2
        y = y_predicted
    return cost


def mpc_controller(y, set_point, u, horizon):

    # Define bounds for control inputs
    bounds = [(u_min, u_max)] * horizon

    setpoint_sequence = [set_point] * horizon

    # Set initial control sequence
    # u_sequence_initial = np.zeros(horizon)
    u_sequence_initial = [u] * horizon

    # Define optimization problem
    optimization_result = minimize(
        cost_function,
        u_sequence_initial,
        args=(y, setpoint_sequence),
        bounds=bounds,
        method='SLSQP',
        options={'maxiter': 10}
    )

    # Extract optimal control sequence
    u_sequence_optimal = optimization_result.x

    # Return next optimal control input
    return u_sequence_optimal[0]



def system_model2(y, u):
    delta_y = (-1 / T) * y + (K / T) * u
    y += delta_y * H
    return y

def papor():
    horizon = 10
    process_variable = 0
    set_point = 2
    control_variable = 0
    for i in range(200):
        control_variable = mpc_controller(process_variable, set_point, control_variable, horizon)
        process_variable = system_model2(process_variable, control_variable)
        print("y =", process_variable)

profile.run('papor()')
