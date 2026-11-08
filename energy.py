GRAVITY = 9.81

import math

# note: pump loss = 1 - pump_efficiency

def calc_head_loss(friction_factor, pipe_length, pipe_diameter, flow_rate):
    fluid_velocity = flow_rate / ((math.pi * pipe_diameter ** 2) / 4)
    return friction_factor * (pipe_length / pipe_diameter) * (fluid_velocity ** 2) / (2 * GRAVITY)

def calc_pipe_friction(fluid_mass, head_loss):
    return fluid_mass * GRAVITY * head_loss

def calc_pump_energy(fluid_mass, height, exit_velocity, pipe_friction):
    energy = (fluid_mass * GRAVITY * height) + (0.5 * fluid_mass * exit_velocity ** 2) + pipe_friction