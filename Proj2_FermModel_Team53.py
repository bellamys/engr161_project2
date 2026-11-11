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
# This program loads in the layout data, then calculates flow rates, fluid
# densities, energy loss, and cost of the specified configuration.
#
#

import Proj2_EnergyCalcs_Team53 as energy
import csv
import Proj2_MassCalcs_Team53 as mass_calcs
import yaml # external package: https://github.com/yaml/pyyaml/

# "universal" constants
TIME = 24*3600
DISCHARGE_COEFF = 0.65

# additional configuration values
PUMP_EPM = '27'
PUMP_GRADE = 'Cheap'
BUILDING_COSTS = 1810000
VOLUME = 4215.43 # 4 11600 gal trucks per hour

# units are 'Scrap', 'Average', 'Premium', or 'World-class'
FERMENTER = 'Average'
DISTILLER = 'World-class'
REMOVAL_UNITS = 'Scrap'

pipes = []
bends = []
cost = [0, 0, 0, 0, 0]

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

    # use csv package to read as list
    with open(f"{type}_table.csv", 'r', encoding = 'utf-8-sig') as fid:
        read = csv.reader(fid)
        vals = list(read)

    column = vals[0].index(quality)
    row = [rws[-1] for rws in vals].index(parameter)

    # returns specified attributes
    return [float(vals[1][column]), float(vals[row][column])]

# parse yaml data
# layout file contains info of used parts
with open('layout.yml', 'r') as fid: 
    main_layout_data = yaml.load(fid, Loader=yaml.SafeLoader)

with open('waste_layout.yml', 'r') as fid: 
    waste_layout_data = yaml.load(fid, Loader=yaml.SafeLoader)

# part_config file contains info from the machine tables
with open('part_config.yml', 'r') as fid:
    part_data = yaml.load(fid, Loader=yaml.SafeLoader)

# calculates the cost and energy loss from a layout specified in / read from a yaml file
def calc_layout(layout_data, energy_loss, cost):
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
            energy_loss[0] += energy.calc_pipe_friction_loss(fluid_d[i], TIME, float(pipe_vals[0]), flow_rate[i], float(pipe[2]), float(pipe[1]))
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
            energy_loss[1] += energy.calc_bend_loss(fluid_d[i], flow_rate[i], TIME, float(bend_vals[0]), float(bend[1]))
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
            valve = layout_data[current_key]['valves'][j]
            # print(valve)
            # gets additional valve attributes from table
            valve_vals = get_values("valve", valve[0], valve[1])
            # adds energy loss and cost from valve
            energy_loss[2] += energy.calc_valve_energy_loss(fluid_d[i], TIME, flow_rate[i], float(valve_vals[0]), float(valve[1]))
            cost[2] += valve_vals[1]
            j += 1
        # print(f"For valves at stage {i}, the energy loss is {energy_loss[2]} and the cost is {cost[2]}.\n")
        i += 1

# gets table attributes from pump
pump = get_values('pump', PUMP_GRADE, PUMP_EPM)

# mass flow rate at each stage in the process (or, after each machine)
mass_flows = [mass_calcs.initMassFlow(VOLUME)]
mass_flows.append(mass_calcs.fermMassFlow(part_data['fermenter'][FERMENTER]['efficiency'], mass_flows[-1]))
mass_flows.append(mass_calcs.filtMassFlow(part_data['material_removal'][REMOVAL_UNITS]['efficiency'], mass_flows[-1]))
mass_flows.append(mass_calcs.distMassFlow(part_data['distiller'][DISTILLER]['efficiency'], mass_flows[-1]))
mass_flows.append(mass_calcs.dehyMassFlow(part_data['material_removal'][REMOVAL_UNITS]['efficiency'], mass_flows[-1]))

# calculate fluid density for each mass flow
fluid_d = [mass_calcs.fluidDensity(i) for i in mass_flows]

# assumptions: discharge coefficient is always 0.65, leak radius ranges from .001-.01 m, pressure drop ranges from 50-60psi * pascal conversion factor, num leaks ranges from 0-2
flow_rate = []
total_cost = 0
i = 0
while i < 5:
    leak_info = mass_calcs.leakValues()
    flow_rate.append(mass_calcs.volumetricFlowRate(mass_flows[i], DISCHARGE_COEFF, leak_info))
    # computes cost of waste pumps, fermenter, and distiller since based off of mass flow rates
    if i == 1:
        cost[i] += flow_rate[i] * part_data['fermenter'][FERMENTER]['cost']
    elif i == 2 or i == 4:
        cost[i] += flow_rate[i] * part_data['material_removal'][REMOVAL_UNITS]['cost']
    elif i == 3: 
        cost[i] += flow_rate[i] * part_data['distiller'][DISTILLER]['cost']
    i += 1

# initialize for main layout
main_energy_loss = [0, 0, 0]
main_cost = [0, 0, 0]

# calculate energy/cost for main layout
calc_layout(main_layout_data, main_energy_loss, main_cost)

# intialize for waste layout
waste_energy_loss = [0, 0, 0]
waste_cost = [0, 0, 0]

# calculate energy/cost for waste layout
calc_layout(waste_layout_data, waste_energy_loss, waste_cost)

# find energy into pump based on energy lost by pump
pump_in = sum(main_energy_loss) / float(pump[0])
pump_loss = (1 - float(pump[0])) * pump_in

# print(f"Energy loss: {energy_loss} \nCost: {cost}\n(Format: [pipes, bends, valves])\n")

print(f"Total energy loss: {sum(main_energy_loss) + pump_loss:.2e}\n")

total_energy = pump_in + 3600 * (part_data['fermenter'][FERMENTER]['energy'] + part_data['distiller'][DISTILLER]['energy'] + 2 * part_data['material_removal'][REMOVAL_UNITS]['energy'])
# print(f"Total energy: {total_energy} kJ / day\n")

# calculate output energy from amount of ethanol
percEthanol = mass_calcs.percEthanol(mass_flows[4])
volFlowRate = flow_rate[4] * TIME * 264.172
outputEnergy = percEthanol * (volFlowRate / 264.172) * (21160.18 * 1000)

energy_in = total_energy + sum(waste_energy_loss)

print(f"Percent ethanol: {percEthanol:.1%}\n")

print(f"Volumetric flow in gallons per day: {volFlowRate:.2f} gal / day\n")

print (f"Energy output: {outputEnergy:.2e} kJ / day\n")

print(f"Waste energy loss: {sum(waste_energy_loss):.2e} kJ / day, waste system cost: ${sum(waste_cost):.2f}\n")

print(f"Total energy in: {energy_in:.2e} kJ / day\nEnergy ROI: {outputEnergy / (energy_in):.2f}\nTotal cost: ${sum(cost) + sum(waste_cost) + total_cost + BUILDING_COSTS:.2f}\n")