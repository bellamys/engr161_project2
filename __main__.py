import energy
import mass_calcs
import yaml
import csv

# universal constants
TIME = 24*3600

# configuration constants
FLOW_RATE = 0.01 # fix this, should not be constant
VOLUME = 3000

# units are 'Scrap', 'Average', 'Premium', or 'World-Class'
FERMENTER = 'Scrap'
DISTILLER = 'Scrap'
REMOVAL_UNITS = 'Scrap'

PUMP_EPM = '27'
PUMP_GRADE = 'Cheap'


# pass all numbers as strings

def get_values(type, quality, parameter):
    # ducts hard-coded, as are only type with different format
    if type == "duct":
        if parameter == 1: # parameter for duct is inner diameter
            return 228
        elif parameter == 1.25:
            return 414
        elif parameter == 1.5:
            return 1.5
        else: return 0

    with open(f"{type}_table.csv", 'r', encoding = 'utf-8-sig') as fid:
        read = csv.reader(fid)
        vals = list(read)
    
    column = vals[0].index(quality)
    row = [rws[-1] for rws in vals].index(parameter)

    return [float(vals[1][column]), float(vals[row][column])]

pump = get_values('pump', PUMP_GRADE, PUMP_EPM)

# parse yaml data
# layout file contains info of used parts
with open('layout.yml', 'r') as fid: 
    layout_data = yaml.load(fid, Loader=yaml.SafeLoader)

# part_config file contains info from the machine tables
with open('part_config.yml', 'r') as fid:
    part_data = yaml.load(fid, Loader=yaml.SafeLoader)

# mass flow rate at each stage in the process (or, after each machine)
mass_flows = [mass_calcs.initMassFlow(VOLUME)]
mass_flows.append(mass_calcs.fermMassFlow(part_data['fermenter'][FERMENTER]['efficiency'], mass_flows[-1]))
mass_flows.append(mass_calcs.filtMassFlow(part_data['material_removal'][REMOVAL_UNITS]['efficiency'], mass_flows[-1]))
mass_flows.append(mass_calcs.distMassFlow(part_data['distiller'][DISTILLER]['efficiency'], mass_flows[-1]))
mass_flows.append(mass_calcs.dehyMassFlow(part_data['material_removal'][REMOVAL_UNITS]['efficiency'], mass_flows[-1]))

# calculate fluid density for each mass flow
fluid_d = [mass_calcs.fluidDensity(i) for i in mass_flows]

flow_rate = FLOW_RATE

<<<<<<< HEAD
# assumptions: discharge coefficient is always 0.65, leak radius ranges from .001-.01 m, pressure drop ranges from 50-60psi * pascal conversion factor, num leaks ranges from 0-2
flow1_rate = []
i = 0
while i < 5:
    leak_info = mass_calcs.leakValues()
    flow1_rate.append(mass_calcs.volumetricFlowRate(mass_flows[i], DISCHARGE_COEFF, leak_info))
    print(f"At stage {i}, the flow rate is {flow1_rate[i]}.\n")
    i += 1

energy_loss = [0, 0, 0, 0]
cost = [0, 0, 0, 0]
=======
# initialize arrays
energy_loss = [0, 0, 0]
cost = [0, 0, 0]
>>>>>>> 8dff8f41a451ce8ecb8887b1d87745a8edba8b8c

pipe = [0, 0]
bend = [0, 0]

# testing
# print(part_data)
# print(layout_data)
# print(layout_data['init']['pipes'])

# pipes
i = 0

# calculate energy loss due to pipe friction
while i < 5: # 5 process stages
    j = 0
    # sets key for stage of progress
    current_key = list(layout_data.keys())[i]
    # iterates for each pipe in progress stage
    while (type(layout_data[current_key]['pipes']) != type(None) and j < len(layout_data[current_key]['pipes'])):
       # sets "pipe" variable to the list of pipe data given in layout
       pipe = layout_data[current_key]['pipes'][j]
    #  print(pipe)
       # gets the additional attributes of pipe from the parts catalog table
       pipe_vals = get_values("pipe", pipe[0], pipe[1])
       # adds the effect of the energy loss and cost
       energy_loss[0] += energy.calc_pipe_friction_loss(fluid_d[i], TIME, float(pipe_vals[0]), flow_rate, float(pipe[2]), float(pipe[1]))
       cost[0] += float(pipe_vals[1]) * float(pipe[2]) # cost per m * pipe m
       j += 1
    # print(f"For pipes at stage {i}, the energy loss is {energy_loss[0]} and the cost is {cost[0]}.\n")
    i += 1

# bends

# calculate energy loss due to bends
i = 0
while i < 5: # 5 process stages
    j = 0
    # gets key for current process stage
    current_key = list(layout_data.keys())[i]
    # iterates once for every bend in proces stage
    while (type(layout_data[current_key]['bends']) != type(None) and j < len(layout_data[current_key]['bends'])):
       # sets "bend" variable to the list of bend data given in layout
       bend = layout_data[current_key]['bends'][j]
    #  print(bend)
       # gets additional bend attributes from parts catalog table
       bend_vals = get_values("bend", bend[0], bend[1])
       # adds bend cost and energy loss
       energy_loss[1] += energy.calc_bend_loss(fluid_d[i], flow_rate, TIME, float(bend_vals[0]), float(bend[1]))
       cost[1] += bend_vals[1]
       j += 1
    # print(f"For bends at stage {i}, the energy loss is {energy_loss[1]} and the cost is {cost[1]}.\n")
    i += 1

# valves

# calculate energy loss from valves
i = 0
# iterates once for each of the 5 process stages
while i < 5: 
    j = 0
    # gets key of current process stage
    current_key = list(layout_data.keys())[i]
    # iterates for each valve in process stage
    while (type(layout_data[current_key]['valves']) != type(None) and j < len(layout_data[current_key]['valves'])):
        # sets variable "valve" to list of valve data from layout file
        valve = layout_data[current_key]['valves'][i]
        # print(valve)
        # gets additional valve attributes from table
        valve_vals = get_values("valve", valve[0], valve[1])
        # adds energy loss and cost from valve
        energy_loss[2] += energy.calc_valve_energy_loss(fluid_d[i], TIME, flow_rate, float(valve_vals[0]), float(valve[1]))
        cost[2] += valve_vals[1]
        j += 1
    # print(f"For valves at stage {i}, the energy loss is {energy_loss[2]} and the cost is {cost[2]}.\n")
    i += 1

# find energy into pump based on energy lost by pump
pump_in = sum(energy_loss) / float(pump[0])
pump_loss = (1 - float(pump[0])) * pump_in

print(f"Energy loss: {energy_loss} \nCost: {cost}\n(Format: [pipes, bends, valves])\n")

print(f"Total energy loss: {sum(energy_loss) + pump_loss}\nTotal cost: {sum(cost)}\n")

# sum of total energy is pump input + energy to power each machien
total_energy = pump_in + part_data['fermenter'][FERMENTER]['energy'] + part_data['distiller'][DISTILLER]['energy'] + 2 * part_data['material_removal'][REMOVAL_UNITS]['energy']
print(f"Total energy: {total_energy} kJ / day\n")
