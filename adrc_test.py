import time

import pyadrc

b0 = 0.26816115942028985507246376811594
delta = 0.1
order = 1
t_settle = 0.5714
k_eso = 6
adrc_statespace = pyadrc.StateSpace(order, delta, b0, t_settle, k_eso, r_lim=(0, 4), m_lim=(0, 4))
setpoint = 3
ctrl = 0.


pv = 2
for i in range(100):

    ctrl = adrc_statespace(pv, ctrl, setpoint)
    print(ctrl)
