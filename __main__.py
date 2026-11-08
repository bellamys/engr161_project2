from read_table import get_values
import energy

user_in = -1
pipes = []
bends = []
pump_effs = []

density = float(input("Fluid density? "))
flow_rate = float(input("Flow rate? "))

# 7 pipe bends, 2 75 deg, 5 90 deg

while user_in != 0:
    user_in = input("1 = input pipe\n2 = input bend\n3 = input pump\n4 = input duct\n\n0 = exit\n")
    if user_in == "1":
        print("Inputting pipe")
        pipe_type = input("Pipe type? ")
        pipe_id = input("Inner diameter? (0.10-0.15) ")
        pipe = [get_values("pipe", pipe_type, pipe_id), pipe_id, float(input("pipe length? ")), 5] # last val is time
        pipes.append(pipe)
        # print(energy.calc_pipe_friction_loss(1000, float(input("time? ")), float(pipe[0]), 1, float(input("pipe length? ")), float(pipe_id)))
    elif user_in == "2":
        print("Inputting bend")
        bend_ang = input("Bend angle? ")
        bend_id = input("Inner diameter? (0.10-0.15) ")
        bends.append([get_values("bend", bend_ang, bend_id), bend_id, float(input("time? "))])
    elif user_in == "3":
        print("Inputting pump")
        pump_effs.append(float(input("Pump efficiency? ")))
    elif user_in == "0":
        break

# sum energy and cost
energy_loss = 0
cost = 0
i = 0
while i < len(pipes):
    energy_loss += energy.calc_pipe_friction_loss(density, float(pipes[i][3]), float(pipes[i][0][0]), flow_rate, float(pipes[i][2]), float(pipes[i][1]))
    cost += pipes[i][0][1] * pipes[i][2] # cost per m * pipe m
    i += 1

i = 0
while i < len(bends):
    energy_loss += energy.calc_bend_loss(density, flow_rate, float(bends[i][2]), float(bends[i][0][0]), float(bends[i][1]))
    cost += bends[i][0][1]
    i += 1

# while i < len(pump_effs):
#     energy_loss *= (1 - pump_effs[i])
#     i += 1

print(f"Energy loss: {energy_loss} \nCost: {cost}")