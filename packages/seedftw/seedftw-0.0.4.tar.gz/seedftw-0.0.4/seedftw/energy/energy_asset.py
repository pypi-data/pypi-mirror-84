# -*- coding: utf-8 -*-
"""
Functions related to modelling of energy assets.

This file can also be imported as a module and contains the following
functions:

    * wind_turbine_generator - converts wind speed to power output of a wind turbine
    * solar_pv_generator - convert solar irradiance to the power output of a PV installation


References:
    J. Twidell & T. Weir, Renewable Energy Resources, 2nd edition, 
    Taylor and Francis, 2006

"""

# Import all useful libraries
import numpy as np

def wind_turbine_generator(wind_speed, rated_power=1000, cut_in_wind_speed=5, \
                           rated_wind_speed=12, cut_out_wind_speed=30):
    '''Models the power production curve of a standard wind turbine.
    The model is based upon (Twidell, 2006), pp. 306-307.

    Parameters
    ----------
    wind_speed : np.array
        Wind speed [m/s]
    rated_power : float
        Rated power of the turbine [W] 
        (default: 1000)
    cut_in_wind_speed : float
        Cut-in wind speed of the turbine [m/s]
        (default: 5)
    rated_wind_speed : float
        Rated wind speed of the turbine [m/s]
        (default: 12)
    cut_out_wind_speed : float
        Cut-out wind speed of the turbine [m/s]
        (default: 30)

    Raises
    ------
    None

    Returns
    -------
    power_output : np.array
        Power production corresponding to the values of wind_speed [W]
    '''
    
    k_cubic = np.where((wind_speed>=cut_in_wind_speed) & (wind_speed<rated_wind_speed))
    k_rated = np.where((wind_speed>=rated_wind_speed) & (wind_speed<=cut_out_wind_speed))

    #k_zero = np.where((wind_speed<=cut_in_wind_speed) | (wind_speed>cut_out_wind_speed))
    power_output = np.zeros(np.size(wind_speed))
    
    u_ci_3 = (cut_in_wind_speed**3)
    u_R_3 = (rated_wind_speed**3)
    a = rated_power / (u_R_3 - u_ci_3)
    b = u_ci_3 / (u_R_3 - u_ci_3)
    power_output[k_cubic,]= a * (wind_speed[k_cubic,] ** 3) - b * rated_power
    
    power_output[k_rated,]=rated_power
    
    return power_output

def solar_pv_generator(solar_radiation, rated_power=1000, rated_radiation=1000):
    '''Models the power production curve of a standard solar PV panel.
     The model is based upon a simplified linear model.
    
     Parameters
     ----------
     wind_speed : np.array
         Values of the incident radiation on the panel [W/m^2]
     rated_power : float
         Rated power of the inverter of the PV panel [W] 
         (default: 1000)
     rated_radiation : float
         Values of the design radiation on the panel [W/m^2]
         (default: 1000)
    
     Raises
     ------
     None
    
     Returns
     -------
     power_output : np.array
         Power production corresponding to the values of solar_radiation [W]
    '''
    power_output = rated_power * (solar_radiation / rated_radiation)
     
    # Forcing the output to not exceed the rated power
    k_excess = np.where(power_output>rated_power)
    power_output[k_excess,] = rated_power
     
    return power_output
