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
# This module contains functions to calculate fluid density, flow rate, and
# fluid masses of the ethanol mixture as it travels through the processes.
#

import math
import random

# initial/general functions
densitySugar = 1599
densityEthanol = 789
densityFiber = 1311
densityWater = 997

# calculates initial flow density w/ given densities
def initFluidDensity():
    fluidDensity = .2*densitySugar + .2*densityFiber + .6*densityWater
    return fluidDensity

# calculates initial mass flow for system
def initMassFlow(volume):
    massFlow = (volume * initFluidDensity())/(24*60*60)
    mfSugar = .2 * massFlow
    mfFiber = .2 * massFlow
    mfWater = .6 * massFlow
    mfEthanol = 0 * massFlow
    return [mfWater, mfFiber, mfSugar, mfEthanol]

# calculates total fluid density using percentage of each component in total mass flows
def fluidDensity(massFlows):
    massTotal = totalMassFlowRate(massFlows)
    percWater = massFlows[0] / massTotal
    percFiber = massFlows[1] / massTotal
    percSugar = massFlows[2] / massTotal
    percEthanol = massFlows[3] / massTotal
    fluidDensity = percWater * densityWater + percFiber * densityFiber + \
                   percSugar * densitySugar + percEthanol * densityEthanol
    return fluidDensity

# calculates sum of used components in system
def totalMassFlowRate(massFlows):
    massTotal = 0
    i = 0
    while (i < 4):
        massTotal += massFlows[i]
        i += 1
    return massTotal

# calculates volumetric flow rate, takes into account pipe leakage
def volumetricFlowRate(massFlows, dischargeCoeff, leakValues):
    totFluDensity = fluidDensity(massFlows)
    massTotal = totalMassFlowRate(massFlows)
    pipeLeakage = dischargeCoeff * (math.pi * math.pow(leakValues[0], 2)) * \
                  math.sqrt(2 * (leakValues[1] / totFluDensity))
    volFlowRate = (massTotal / totFluDensity) - (leakValues[2] * pipeLeakage)
    return volFlowRate

# calculates percentage of ethanol produced
def percEthanol(massFlows):
    massTotal = totalMassFlowRate(massFlows)
    ethanolProd = massFlows[3] / massTotal
    return ethanolProd

# generates leak values based off of assumptions
# assumptions: number of leaks ranges between 0 and 1, pressure drop ranges from 50 to 58/59 psi, and leak radius in between 0.001 and 0.005 m
def leakValues():
    pascalConverFac = 6894.75729
    numLeaks = int(random.random() * 2)
    pressureDrop = int((random.random() * 9) + 50) * pascalConverFac
    leakRadius = int(random.random() * 6) * .001
    return [leakRadius, pressureDrop, numLeaks]

# fermenter functions (calculates mass flows after going through fermenter)

def fermMassFlow(fermEff, mfInputs):
    mfWater = mfInputs[0]
    mfFiber = mfInputs[1]
    mfSugar = (1 - fermEff) * mfInputs[2]
    mfEthanol = .51 * mfInputs[2] * fermEff
    mfCO2 = .49 * mfInputs[2] * fermEff
    return [mfWater, mfFiber, mfSugar, mfEthanol, mfCO2]

# filter functions (calculates mass flows after going through filter)

def filtMassFlow(filtEff, mfInputs):
    mfWater = mfInputs[0]
    mfFiber = mfInputs[1] * (1 - filtEff)
    mfSugar = mfInputs[2]
    mfEthanol = mfInputs[3]
    fiberWaste = mfInputs[1] * filtEff
    return [mfWater, mfFiber, mfSugar, mfEthanol, fiberWaste]

# distiller functions (calculates mass flows after going through distiller)

def distMassFlow(distEff, mfInputs):
    mfDenom = mfInputs[0] + mfInputs[1] + mfInputs[2]
    mfWater = (mfInputs[0] * mfInputs[3] * ((1/distEff)-1)) / mfDenom
    mfFiber = (mfInputs[1] * mfInputs[3] * ((1/distEff)-1)) / mfDenom
    mfSugar = (mfInputs[2] * mfInputs[3] * ((1/distEff)-1)) / mfDenom
    mfEthanol = mfInputs[3]
    fiberWaste = mfInputs[1] - mfFiber
    sugarWaste = mfInputs[2] - mfSugar
    waterWaste = mfInputs[0] - mfWater
    return [mfWater, mfFiber, mfSugar, mfEthanol, fiberWaste, sugarWaste, waterWaste]

# dehydrator functions (calculates mass flows after going through dehydrator)

def dehyMassFlow(dehyEff, mfInputs):
    mfWater = mfInputs[0] * (1-dehyEff)
    mfFiber = mfInputs[1]
    mfSugar = mfInputs[2]
    mfEthanol = mfInputs[3]
    waterWaste = mfInputs[0] * dehyEff
    return [mfWater, mfFiber, mfSugar, mfEthanol, waterWaste]
