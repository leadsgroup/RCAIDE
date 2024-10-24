#  RCAIDE/Methods/Energy/Distributors/Electrical_Bus/append_battery_conditions.py
# 
# Created: Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Mission.Common     import   Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  METHODS
# ---------------------------------------------------------------------------------------------------------------------- 
def append_bus_conditions(bus,segment): 
    """ Appends the initial bus conditions
        
        Assumptions:
        N/A
    
        Source:
        N/A
    
        Inputs:  
       
        Outputs:
           
        Properties Used:
        None
        """
    ones_row                                                       = segment.state.ones_row
   
    segment.state.conditions.energy[bus.tag]                       = Conditions()
    segment.state.conditions.energy[bus.tag].battery_modules       = Conditions()
    segment.state.conditions.energy[bus.tag].power_draw            = 0 * ones_row(1)
    segment.state.conditions.energy[bus.tag].SOC                   = 0 * ones_row(1) 
    segment.state.conditions.energy[bus.tag].current_draw          = 0 * ones_row(1)
    segment.state.conditions.energy[bus.tag].charging_current      = 0 * ones_row(1)
    segment.state.conditions.energy[bus.tag].voltage_open_circuit  = 0 * ones_row(1)
    segment.state.conditions.energy[bus.tag].voltage_under_load    = 0 * ones_row(1) 
    segment.state.conditions.energy[bus.tag].heat_energy_generated = 0 * ones_row(1) 
    segment.state.conditions.energy[bus.tag].efficiency            = 0 * ones_row(1)
    segment.state.conditions.energy[bus.tag].temperature           = 0 * ones_row(1)
    segment.state.conditions.energy[bus.tag].energy                = 0 * ones_row(1)
    segment.state.conditions.energy[bus.tag].regenerative_power    = 0 * ones_row(1)
   
    return


def append_bus_segment_conditions(bus,conditions,segment):
    """Sets the initial bus properties at the start of each 
        segment as the last point from the previous segment.  
        It adds the power draw from the thermal management system
        to the first control point power draw.
    
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:  
            bus           (data structure)              [None]
            conditions    (data structure)              [None]
            segment       (data structure)              [None]
        Outputs:
        None
    
        Properties Used:
        None
    """    

    bus_conditions             = conditions[bus.tag]
    ones_row                   = segment.state.ones_row
    bus_conditions.power_draw  = 0 * ones_row(1)
    
    if segment.state.initials:
        for network in segment.analyses.energy.vehicle.networks:
            for coolant_line in  network.coolant_lines:
                for tag, item in  coolant_line.items():
                    if tag == 'battery_modules':
                        for battery in item:
                            for btms in  battery:
                                bus_conditions.power_draw[0,0]   +=  segment.state.initials.conditions.energy[coolant_line.tag][btms.tag].power[-1] 
                    if tag == 'heat_exchangers':
                        for heat_exchanger in  item:                    
                            bus_conditions.power_draw[0,0]   +=  segment.state.initials.conditions.energy[coolant_line.tag][heat_exchanger.tag].power[-1] 
    return