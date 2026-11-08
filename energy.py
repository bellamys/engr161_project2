GRAVITY = 9.81

# nums from outside/based on factory: pipe length, bend angles, needed height

import math

# note: pump loss = 1 - pump_efficiency

def calc_pump_energy(fluid_mass, height, exit_velocity, pipe_friction):
    return (fluid_mass * GRAVITY * height) + (0.5 * fluid_mass * exit_velocity ** 2) + pipe_friction

def calc_head_loss(fric, flow_rate, pipe_length, pipe_id):
    return (fric * (8 / math.pi ** 2) * ((flow_rate ** 3 * pipe_length) / pipe_id ** 5))

def calc_pipe_friction_loss(density, d_t, fric, flow_rate, pipe_length, pipe_id):
    return density * d_t * calc_head_loss(fric, flow_rate, pipe_length, pipe_id)

def calc_bend_loss(density, flow_rate, d_t, bend_fac, pipe_id):
    return (density * flow_rate * d_t) * (bend_fac * (flow_rate / (math.pi * (pipe_id / 2) ** 2) ** 2 / 2))