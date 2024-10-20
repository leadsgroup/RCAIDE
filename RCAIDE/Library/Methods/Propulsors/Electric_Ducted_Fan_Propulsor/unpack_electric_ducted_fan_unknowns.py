# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/unpack_electric_ducted_fan_unknowns.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke   

# ---------------------------------------------------------------------------------------------------------------------- 
#  unpack electric ducted_fan network unknowns 
# ----------------------------------------------------------------------------------------------------------------------  

def unpack_electric_ducted_fan_unknowns(propulsor,reference_propulsor,segment,bus): 
    bus_results = segment.state.conditions.energy[bus.tag]
    motor       =  propulsor.motor  
    bus_results[propulsor.tag][motor.tag].rotor_power_coefficient = segment.state.unknowns[reference_propulsor.tag  + '_ducted_fan_cp'] 
    return 