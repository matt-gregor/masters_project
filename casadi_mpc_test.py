import time

import casadi as ca
import numpy as np

# Define system dynamics
A = np.array([[-0.2899]])
B = np.array([[1]])
C = np.array([[0.2682]])
D = np.array([[0.0]])

# Define MPC parameters
N = 10  # Prediction horizon
dt = 0.1  # Sampling time

# Define optimization variables
u = ca.MX.sym('u')  # Control input
x = ca.MX.sym('x')  # State

# Define state and control bounds
u_min = 0.0
u_max = 4.0
x_min = 0.0
x_max = 4.0

# Define cost function weights
Q = np.eye(1)  # State tracking weight matrix
R = np.eye(1)  # Control effort weight matrix

# Create symbolic variables for states and controls over the prediction horizon
U = ca.MX.sym('U', N)  # Control trajectory
X = ca.MX.sym('X', N + 1)  # State trajectory

# Define constraints
constraints = [
    X[0] - x,  # Initial state constraint
    X[N] - 0.0  # Terminal state constraint
]

# Define objective function
cost = 0.0
for i in range(N):
    cost += ca.mtimes([(X[i] - x).T, Q, X[i] - x]) + ca.mtimes([(U[i] - u).T, R, U[i] - u])

# Concatenate state and control trajectories
XU = ca.vertcat(X, U)


# Define optimization problem
optimization_parameters = ca.vertcat(x, u)

# Declare inputs for objective and constraints
inputs = [XU] + [optimization_parameters[i] for i in range(optimization_parameters.numel())]

objective = ca.Function('f', inputs, [cost])
constraints = ca.Function('g', inputs, [ca.vertcat(*constraints)])





nlp = {'x': optimization_parameters, 'f': objective(optimization_parameters), 'g': constraints(optimization_parameters)}
opts = {'ipopt.tol': 1e-4, 'ipopt.print_level': 0, 'print_time': 0, 'ipopt.max_iter': 100}

solver = ca.nlpsol('solver', 'ipopt', nlp, opts)

# MPC loop
x0 = 2.0  # Initial state
N_sim = 20  # Number of MPC iterations

for i in range(N_sim):
    # Set initial state and solve the optimization problem
    x_init = np.concatenate((np.full(N+1, x0), np.zeros(N)))
    lbx = np.concatenate((x_min*np.ones(N+1), u_min*np.ones(N)))
    ubx = np.concatenate((x_max*np.ones(N+1), u_max*np.ones(N)))
    lbg = np.zeros(N+1)
    ubg = np.zeros(N+1)

    sol = solver(x0=x_init, lbx=lbx, ubx=ubx, lbg=lbg, ubg=ubg)

    # Extract optimal control input
    u_opt = sol['x'][N]

    # Apply control input to the system (simulate one step)
    x0 = A.dot(x0) + B.dot(u_opt)

    print(f"Iteration {i+1}: u_opt = {u_opt}, x = {x0}")



# def system_model(y, u):
#     delta_y = (-1 / T) * y + (K / T) * u
#     y += delta_y * H
#     return y


# def system_model1(y, u):
#     global next
#     y = next
#     delta_y = (-1 / T) * y + (K / T) * u
#     next += delta_y * H
#     return y

# horizon = 5
# process_variable = 0
# set_point = 2
# control_variable = 0
# next = process_variable

# K = 0.925156  # Gain
# T = 3.45  # Time constant
# T0 = 0.1  # Dead time
# H = 0.1  # Sampling time

# for i in range(200):
#     control_variable = mpc_controller2(process_variable, set_point, control_variable, horizon)
#     process_variable = system_model1(process_variable, control_variable)
#     print("y =", process_variable, " cv =", control_variable)

