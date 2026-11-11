# File: __main__.py
# Date: 11/10/2026
# By: Danica Libanan
# dlibanan
# Savannah Bellamy
# bellamys
# Madison Armstrong
# armst236
# Braxton Shoults
# bshoult
# Section: 3
# Team: 53
#
# ELECTRONIC SIGNATURE
# Danica Libanan
# Savannah Bellamy
# Madison Armstrong
# Braxton Shoults
#
# The electronic signatures above indicate that the program
# submitted for evaluation is the combined effort of all
# team members and that each member of the team was an
# equal participant in its creation. In addition, each
# member of the team has a general understanding of
# all aspects of the program development and execution.
#
# This program contains functions to calculate energy loss for each part included in the factory.
#
#
GRAVITY = 9.81

import math

# note: pump loss = 1 - pump_efficiency

# pipe energy loss
def calc_head_loss(fric, flow_rate, pipe_length, pipe_id):
    return (fric * (8 / math.pi ** 2) * ((flow_rate ** 2 * pipe_length) / pipe_id ** 5)) / 1000

def calc_pipe_friction_loss(density, d_t, fric, flow_rate, pipe_length, pipe_id):
    return density * d_t * calc_head_loss(fric, flow_rate, pipe_length, pipe_id)

# bend energy loss
def calc_bend_loss(density, flow_rate, d_t, bend_fac, pipe_id):
    return (density * flow_rate * d_t) * (bend_fac * (flow_rate / (math.pi * (pipe_id / 2) ** 2) ** 2 / 2)) / 1000

# valve energy loss
def calc_valve_head_loss(coeff, flow_rate, pipe_id):
    return (coeff * (flow_rate / (math.pi * (pipe_id / 2) ** 2) ** 2)) / 2

def calc_valve_energy_loss(density, d_t, flow_rate, coeff, pipe_id):
    return density * d_t * flow_rate * calc_valve_head_loss(coeff, flow_rate, pipe_id) / 1000