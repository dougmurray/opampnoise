""" General opamp circuit noise analysis.

This is not an exhausitive opamp noise analysis, but instead considers
only the most dominante noise sources for quick evaluation.  Included are
helper functions to determine which noise sources are most dominate.  

Author: Douglass Murray

"""
import numpy as np

def inverting_opamp_gain(feedback_res, g_res):
    """
    Returns the gain (V/V) of inverting opamp circuit.

    Parameters
    ----------
    feedback_res : float
        Resistance in Ohms of feedback resistor.
    g_res : float
        Resistance in Ohms of resistor from inverting to ground.
    
    Returns
    -------
    inv_gain : float
        Gain of inverting opamp circuit in V/V.
    
    """
    inv_gain = feedback_res / g_res
    
    return inv_gain

def parallel_res(res_one, res_two):
    """
    Returns the equivalent resistance in Ohms of resistors in parallel.

    Parameters
    ----------
    res_one : float
        Resistance in Ohms of first resistor.
    res_two : float
        Resistance in Ohms of second resistor.
    
    Returns
    -------
    parallel_res : float
        Equivalent resistance in Ohms.
    
    """
    parallel_res = (res_one * res_two) / (res_one + res_two)
    
    return parallel_res

def resistor_thermal_noise(res):
    """
    Returns the thermal noise of resistor at room temp.

    This is the standard Johnson-Nyquist noise.

    Parameters
    ----------
    res : float
        Resistance in Ohms of resistor.
    
    Returns
    -------
    thermal_noise : float
        Intrinsic thermal noise of resitor in V/sqrt(Hz).
    
    """
    k = 1.38e-23 # J/K, Boltzmann constant
    temp = 289 # K, room temperature
    thermal_noise = np.sqrt(4 * k * temp * res)
    
    return thermal_noise

def noise_gain(feedback_res, res_g):
    """
    Returns the noise gain of a opamp circuit.
    
    This is always 1 + Rf/Rg, regardless of opamp configuration.

    Parameters
    ----------
    feedback_res : float
        Resistance of feedback resistor in Ohms.
    res_g : float
        Resistance of resistor to ground in Ohms.
    
    Returns
    -------
    gain_of_noise : float
        The noise gain (1 + Rf/Rg) of opamp circuit.
    
    """
    gain_of_noise = 1 + feedback_res / res_g # ALWAYS! Regardless of opamp config
    
    return gain_of_noise

def opamp_circuit_current_noise(feedback_res, g_res, opamp_input_current_noise):
    """
    Returns the current noise of a opamp circuit.
    
    This noise, in V/sqrt(Hz), is derived from the current noise of the opamp
    going through the feedback resistors.  This current produces voltag noise,
    via Ohm's Law.  

    Parameters
    ----------
    feedback_res : float
        Resistance of feedback resistor in Ohms.
    res_g : float
        Resistance of resistor to ground in Ohms.
    opamp_input_current_noise : float
        Input current noise of opamp in A/sqrt(Hz).
    
    Returns
    -------
    current_noise : float
        The current noise in V/sqrt(Hz).
    
    """
    Req = parallel_res(feedback_res, g_res)
    current_noise = Req * opamp_input_current_noise
    
    return current_noise

def opamp_broadband_noise(opamp_GBW, noise_gain, filter_order=1.57):
    """
    Returns the broadband noise of a opamp circuit in Hz.
    
    For noise analysis, this frequency is incorrect to use if filtering is
    involved. For example, if there is an RC filter after the opamp circuit, 
    or if there is a capacitor in the feedback, the proper frequency to use 
    for noise calculations is the filter frequency.   

    Parameters
    ----------
    opamp_GBW : float
        Gain Bandwidth Product of opamp in Hz.
    noise_gain : float
        Noise gain of opamp circuit, which is always just (1 + Rf/Rg).
    filter_order : float
        Filter order of circuit. Default is 1.57, first order filter.
    
    Returns
    -------
    broadband_noise_freq : float
        The broadband noise in Hz.
    
    """
    broadband_noise_freq = filter_order * (opamp_GBW / noise_gain) # Hz
    
    return broadband_noise_freq

def total_input_noise_rms(opamp_input_voltage_noise, opamp_input_current_noise, 
                          feedback_res, g_res, opamp_GBW, filter_res=None, filter_cap=None):
    """
    Returns the total input voltage noise in Vrms of opamp circuit.
    
    This combines all the noise courses, adding them in quadrature. If there 
    is filtering this function uses the filter corner frequency as the 
    bandwidth limiting frequency.

    Parameters
    ----------
    opamp_input_voltage_noise : float
        Input voltage noise of opamp in V/sqrt(Hz).
    opamp_input_current_noise : float
        Input current noise of opamop in A/sqrt(Hz).
    feedback_res : float
        Resistance of feedback resistor in Ohms.
    g_res : float
        Resistance of resistor to ground in Ohms.
    opamp_GBW : float
        Gain Bandwidth Product of opamp in Hz.
    filter_res : float
        Resistance of filter resistor in Ohms.  Default is None.
    filter_cap : float
        Capacitance of filter capacitor in F.  Default is None.
    
    Returns
    -------
    total_input_voltage_noise : float
        Total input voltage noise in Vrms.
    
    """
    current_noise = parallel_res(feedback_res, g_res) * opamp_input_current_noise
    resistors_voltage_noise = resistor_thermal_noise(parallel_res(feedback_res, g_res))
    opamp_noise_gain = noise_gain(feedback_res, g_res)
    broadband_noise = opamp_broadband_noise(opamp_GBW, opamp_noise_gain) # Hz
    if not (filter_res or filter_cap):
        total_input_voltage_noise = np.sqrt(opamp_input_voltage_noise**2 
                                            + current_noise**2 
                                            + resistors_voltage_noise**2) * np.sqrt(broadband_noise) # Vrms
        print(f"At bandwidth of: {broadband_noise} Hz") 
    else:
        rc_freq = 1 / (2 * np.pi * filter_res * filter_cap) # Hz
        if rc_freq > broadband_noise:
            total_input_voltage_noise = np.sqrt(opamp_input_voltage_noise**2 
                                            + current_noise**2 
                                            + resistors_voltage_noise**2) * np.sqrt(broadband_noise) # Vrms
            print(f"At bandwidth of: {broadband_noise} Hz")
        else:
            total_input_voltage_noise = np.sqrt(opamp_input_voltage_noise**2 
                                                         + current_noise**2 
                                                         + resistors_voltage_noise**2) * np.sqrt(1.57 * rc_freq) # Vrms
            print(f"At bandwidth of: {rc_freq} Hz") 
    
    return total_input_voltage_noise

def total_output_noise_rms(input_voltage_noise, opamp_gain):
    """
    Returns the total output voltage noise in Vrms of opamp circuit.
    
    Calculated by multiplying the total input voltage noise by the gain
    of the opamp circuit.  Good meteric for comparing the noise of 
    opamp circuits.

    Parameters
    ----------
    input_voltage_noise : float
        Total Input voltage noise of opamp circuit in Vrms.
    opamp_gain : float
        Gain of opamop circuit.
    
    Returns
    -------
    total_output_voltage_noise : float
        Total output voltage noise in Vrms.
    
    """
    total_output_voltage_noise = input_voltage_noise * opamp_gain # Vrms
    
    return total_output_voltage_noise

def resistor_or_opamp_noise_dominant(feedback_res, g_res, opamp_input_voltage_noise):
    """
    Returns a boolean signifying that the opamp voltage input noise is dominant 
    over the resistors' noise.
    
    In general it is best to ensure that the opamp input voltage noise
    is dominant over the resistors' noise.

    Parameters
    ----------
    feedback_res : float
        Resistance of feedback resistor in Ohms.
    g_res : float
        Resistance of resistor to ground in Ohms.
    opamp_input_voltage_noise : float
        Input voltage noise of opamp in V/sqrt(Hz).
    
    Returns
    -------
    ignore_resistor_noise : boolean
        If True then opamp input voltage noise is dominant over resistors' noise.
    
    """
    resistors_voltage_noise = resistor_thermal_noise(parallel_res(feedback_res, g_res))
    # Is resistor noise or opamp voltage noise dominant
    if (3 * resistors_voltage_noise) > opamp_input_voltage_noise:
        print("\nBad, resistor noise is dominant over opamp voltage noise.")
        print("Try to reduce feedback resistor values.")
        print("Low noise opamp not necessary.")
        ignore_resistor_noise = False # cannot ignore the resistor noise
    elif opamp_input_voltage_noise > (3 * resistors_voltage_noise):
        print("\nGood, opamp voltage noise is dominant over resistor noise.")
        print("Ensure to use a low noise opamp.")
        ignore_resistor_noise = True
    else:
        print("\nNeither opamp votlage noise nor resistor noise is dominant.")
        ignore_resistor_noise = False # cannot ignore the resistor noise
    
    return ignore_resistor_noise

def current_noise_or_opamp_noise_dominant(feedback_res, g_res, opamp_input_current_noise, opamp_input_voltage_noise):
    """
    Returns a boolean signifying that the opamp voltage input noise is dominant 
    over the current noise.
    
    In general it is best to ensure that the opamp input voltage noise
    is dominant over the current noise.

    Parameters
    ----------
    feedback_res : float
        Resistance of feedback resistor in Ohms.
    g_res : float
        Resistance of resistor to ground in Ohms.
    opamp_input_current_noise : float
        Input current noise of opamp in A/sqrt(Hz)
    opamp_input_voltage_noise : float
        Input voltage noise of opamp in V/sqrt(Hz).
    
    Returns
    -------
    ignore_current_noise : boolean
        If True then opamp input voltage noise is dominant over current noise.
    
    """
    input_current_noise = opamp_circuit_current_noise(feedback_res, g_res, opamp_input_current_noise)
    # Is current or voltage noise dominant
    if opamp_input_voltage_noise > (3 * input_current_noise):
        print("\nOpamp noise dominant over current noise.")
        ignore_current_noise = True
    elif (3 * input_current_noise) > opamp_input_voltage_noise:
        print("\nCurrent noise dominant over voltage noise.")
        print("Try to reduce feedback resistor values.")
        print("Try using a JFET/CMOS opamp.")
        ignore_current_noise = False # cannot ignore the current noise 
    else:
        print("\nNeither current nor voltage noise is dominant.")
        ignore_current_noise = False # cannot ignore the current noise
    
    return ignore_current_noise

def broadband_or_white_noise_dominant(feedback_res, g_res, opamp_GBW, opamp_freq_corner):
    "Determines whether broadband noise or 1/f noise is dominant noise source.  Usually it is broadband."
    """
    Returns a boolean signifying that the 1/f  noise is dominant 
    over the broadband noise.
    
    In general, unless the signal frequency range is below 10 kHz,
    you can ignore the 1/f noise.

    Parameters
    ----------
    feedback_res : float
        Resistance of feedback resistor in Ohms.
    g_res : float
        Resistance of resistor to ground in Ohms.
    opamp_GBW : float
        Gain Bandwidth Product of opamp in Hz.
    opamp_freq_corner : float
        Corner frequency of opamp input voltage noise in Hz.  Based on opamp noise density graph.
    
    Returns
    -------
    ignore_one_over_f__noise : boolean
        If True then 1/f noise is dominant over broadband noise.
    
    """
    # Is broadband or 1/f noise dominant (protip, if bandwidth > 10kHz, ignore 1/f)
    opamp_noise_gain = noise_gain(feedback_res, g_res)
    broadband_noise_freq = opamp_broadband_noise(opamp_GBW, opamp_noise_gain)
    if broadband_noise_freq > (10 * opamp_freq_corner):
        print("\nBroadband noise is dominant over 1/f noise.")
        print(f"Broadband noise: {broadband_noise_freq} Hz")
        ignore_one_over_f__noise = True
    elif (10 * opamp_freq_corner) > broadband_noise_freq:
        print("\n1/f noise is dominant over broadband noise.")
        print("Ensure to use low 0.1 Hz to 10 Hz noise opamp!")
        ignore_one_over_f__noise = False
    else:
        print("\nNeither broadband nor 1/f noise dominant.")
        ignore_one_over_f__noise = False
    
    return ignore_one_over_f__noise

if __name__ == "__main__":
    import argparse

    my_parser = argparse.ArgumentParser(prog='opampnoise', 
                                        description='Total opamp circuit output noise')
    my_parser.add_argument('opamp_input_voltage_noise', 
                           metavar='opamp_input_voltage_noise', 
                           type=float, nargs='?', default=1.0e-9,  
                           help='opamp input voltage noise')
    my_parser.add_argument('opamp_input_current_noise', 
                           metavar='opamp_input_current_noise', 
                           type=float, nargs='?', default=21.7e-12, 
                           help='opamp input current noise')
    my_parser.add_argument('opamp_GBW', metavar='opamp_GBW', 
                           type=float, nargs='?', default=80e6, 
                           help='opamp gain bandwidth')
    my_parser.add_argument('opamp_freq_corner', metavar='opamp_freq_corner', 
                           type=float, nargs='?', default=20, 
                           help='opamp noise corner freq (from graph)')
    my_parser.add_argument('res_feedback', metavar='res_feedback', 
                           type=float, nargs='?', default=100e3, 
                           help='feedback resistance')
    my_parser.add_argument('res_g', metavar='res_g', 
                           type=float, nargs='?', default=1e3, 
                           help='res_g resistance')
    my_parser.add_argument('filter_res', metavar='filter_res', 
                           type=float, nargs='?', default=5e3,
                           help='filter resistance, if any')
    my_parser.add_argument('filter_cap', metavar='filter_cap', 
                           type=float, nargs='?', default=4.7e-9,
                           help='filter capacitance or cap on feedback res, if any')
    args = my_parser.parse_args()
    
    # Opamp circuit specs
    opamp_input_voltage_noise = args.opamp_input_voltage_noise
    opamp_input_current_noise = args.opamp_input_current_noise
    opamp_GBW = args.opamp_GBW
    opamp_freq_corner = args.opamp_freq_corner
    res_feedback = args.res_feedback
    res_g = args.res_g
    filter_res = args.filter_res
    filter_cap = args.filter_cap
    opamp_gain = inverting_opamp_gain(res_feedback, res_g)
    
    total_input_noise = total_input_noise_rms(opamp_input_voltage_noise, 
                                              opamp_input_current_noise, 
                                              res_feedback, res_g, 
                                              opamp_GBW, 
                                              filter_res=filter_res, 
                                              filter_cap=filter_cap)
    total_output_noise = total_output_noise_rms(total_input_noise, opamp_gain)
    # print(f"Total input noise: {total_input_noise} Vrms")
    print(f"Total output noise: {total_output_noise} Vrms")
    
    # Checks on which noise sources are dominant
    resistor_or_opamp_noise_dominant(res_feedback, res_g, opamp_input_voltage_noise)
    current_noise_or_opamp_noise_dominant(res_feedback, res_g, opamp_input_current_noise, opamp_input_voltage_noise)
    broadband_or_white_noise_dominant(res_feedback, res_g, opamp_GBW, opamp_freq_corner)