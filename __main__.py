from read_table import get_values
import energy
import mass_calcs
import yaml

TIME = 24*3600
DISCHARGE_COEFF = 0.65

user_in = -1
pipes = []
bends = []
pump_effs = []

# 7 pipe bends, 2 75 deg, 5 90 deg

# parse yaml data
with open('layout.yml', 'r') as fid:
    layout_data = yaml.load(fid, Loader=yaml.SafeLoader)

with open('part_config.yml', 'r') as fid:
    part_data = yaml.load(fid, Loader=yaml.SafeLoader)

mass_flows = [mass_calcs.initMassFlow(part_data['volume'])]
mass_flows.append(mass_calcs.fermMassFlow(part_data['fermenter_eff'], mass_flows[-1]))
mass_flows.append(mass_calcs.filtMassFlow(part_data['filter_eff'], mass_flows[-1]))
mass_flows.append(mass_calcs.distMassFlow(part_data['distiller_eff'], mass_flows[-1]))
mass_flows.append(mass_calcs.dehyMassFlow(part_data['dehydrator_eff'], mass_flows[-1]))
fluid_d = [mass_calcs.fluidDensity(i) for i in mass_flows]

flow_rate = part_data['flow_rate']

energy_loss = [0, 0, 0, 0]
cost = [0, 0, 0, 0]

print(part_data)
print(layout_data)
print(layout_data['init']['pipes'])

# pipes
i = 0

while i < 5: # 5 process stages
    j = 0
    current_key = list(layout_data.keys())[i]
    while (type(layout_data[current_key]['pipes']) != type(None) and j < len(layout_data[current_key]['pipes'])):
       pipe = layout_data[current_key]['pipes'][j]
       pipe_vals = get_values("pipe", pipe[0], pipe[1])
       energy_loss[0] += energy.calc_pipe_friction_loss(fluid_d[i], TIME, float(pipe_vals[0]), flow_rate, float(pipe[2]), float(pipe[1]))
       print(f"{pipe_vals[1]}, {pipe[1]}\n")
       cost[0] += float(pipe_vals[1]) * float(pipe[1]) # cost per m * pipe m
       print(f"For pipes at stage {i}, the energy loss is {energy_loss[0]} and the cost is {cost[0]}.\n")
       j += 1
    i += 1

# bends

i = 0
while i < 5: # 5 process stages
    j = 0
    current_key = list(layout_data.keys())[i]
    while (type(layout_data[current_key]['bends']) != type(None) and j < len(layout_data[current_key]['bends'])):
       bend = layout_data[current_key]['bends'][j]
       bend_vals = get_values("bend", bend[0], bend[1])
       energy_loss[1] += energy.calc_pipe_friction_loss(fluid_d[i], TIME, float(pipe_vals[0]), flow_rate, float(pipe[2]), float(pipe[1]))
       print(f"{bend_vals[1]}, {bend[1]}\n")
       cost[1] += float(bend_vals[1]) * float(bend[1]) # cost per m * pipe m
       print(f"For bends at stage {i}, the energy loss is {energy_loss[1]} and the cost is {cost[1]}.\n")
       j += 1
    i += 1

# valves
'''
i = 0
while i < 5: 
    j = 0
    current_key = list(layout_data.keys())[i]
    while (type(layout_data[current_key]['valves']) != type(None) and j < len(layout_data[current_key]['valves'])):
        valve = layout_data[current_key]['valves'][i]
        valve_vals = get_values("valve", valve[0], valve[1])
        energy_loss += energy.calc_bend_loss(fluid_d[i], flow_rate, TIME, float(valve[2]), float(valve[1])) # valve energy loss uses same eq as bend energy loss
        print(f"{valve_vals[1]}, {valve[1]}\n")
        cost += float(valve_vals[1]) * float(valve[1])
        print(f"At stage {i}, the energy loss is {energy_loss} and the cost is {cost}.\n")
        j += 1
    i += 1
'''

# pumps
'''
i = 0
while i < 5: 
    j = 0
    current_key = list(layout_data.keys())[i]
    while (type(layout_data[current_key]['pumps']) != type(None) and j < len(layout_data[current_key]['pumps'])):
        pump = layout_data[current_key]['pumps'][i]
        pump_vals = get_values("pump", pump[0], pump[1])
        energy_loss += energy. # i'm not sure how you want pump loss to be calculated
        print(f"{pump_vals[1]}, {pump[1]}\n")
        cost += float(pump_vals[1]) * float(pump[1])
        print(f"At stage {i}, the energy loss is {energy_loss} and the cost is {cost}.\n")
        j += 1
    i += 1
'''
# after pump

'''
while user_in != 0:
    user_in = input("1 = input pipe\n2 = input bend\n3 = input pump\n4 = input duct\n\n0 = exit\n")
    if user_in == "1":
        print("Inputting pipe")
        pipe_type = input("Pipe type? ")
        pipe_id = input("Inner diameter? (0.10-0.15) ")
        pipe = [get_values("pipe", pipe_type, pipe_id), pipe_id, float(input("pipe length? ")), TIME] # last val is time
        pipes.append(pipe)
        # print(energy.calc_pipe_friction_loss(1000, float(input("time? ")), float(pipe[0]), 1, float(input("pipe length? ")), float(pipe_id)))
    elif user_in == "2":
        print("Inputting bend")
        bend_ang = input("Bend angle? ")
        bend_id = input("Inner diameter? (0.10-0.15) ")
        bends.append([get_values("bend", bend_ang, bend_id), bend_id, TIME])
    elif user_in == "3":
        print("Inputting pump")
        pump_effs.append(float(input("Pump efficiency? ")))
    elif user_in == "0":
        break

# set up densities
# fluid_d = [mass_calcs.initFluidDensity]
'''

# ferm, filter, dist, deh
'''
process_pipes = [int(input("Number of pipes before fermenter? "))]
process_pipes.append(int(input("Number of pipes before filter? ")))
process_pipes.append(int(input("Number of pipes before distiller? ")))
process_pipes.append(int(input("Number of pipes before dehydrator? ")))
process_pipes.append(int(input("Number of pipes after dehydrator? ")))

process_bends = [int(input("Number of bends before fermenter? "))]
process_bends.append(int(input("Number of bends before filter? ")))
process_bends.append(int(input("Number of bends before distiller? ")))
process_bends.append(int(input("Number of bends before dehydrator? ")))
process_bends.append(int(input("Number of bends after dehydrator? "))) 

# sum energy and cost
energy_loss = 0
cost = 0
i = 0
process_point = 0

while i < len(pipes):
    energy_loss += energy.calc_pipe_friction_loss(fluid_d[process_point], float(pipes[i][3]), float(pipes[i][0][0]), flow_rate, float(pipes[i][2]), float(pipes[i][1]))
    cost += pipes[i][0][1] * pipes[i][2] # cost per m * pipe m
    if i == sum(process_pipes[:process_point]): process_point += 1
    i += 1

i = 0
process_point = 0
while i < len(bends):
    energy_loss += energy.calc_bend_loss(fluid_d[process_point], flow_rate, float(bends[i][2]), float(bends[i][0][0]), float(bends[i][1]))
    cost += bends[i][0][1]
    if i == sum(process_bends[:process_point]): process_point += 1
    i += 1


# while i < len(pump_effs):
#     energy_loss *= (1 - pump_effs[i])
#     i += 1


i = 0
process_point = 0
while i < len(pipes):
    energy_loss += energy.calc_head_loss(float(pipes[i][0][0]), flow_rate, float(pipes[i][2]), float(pipes[i][1]))
    i += 1
'''
print(f"Energy loss: {energy_loss} \nCost: {cost}")