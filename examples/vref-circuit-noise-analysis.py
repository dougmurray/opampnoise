import opampnoise as opn
import numpy as np
import matplotlib.pyplot as plt

# Opamps used
ada4522_input_voltage_noise = 5.8e-9 # V/sqrt(Hz)
ada4522_input_current_noise = 0.8e-12 # A/sqrt(Hz)
ada4522_GBW = 2.7e6 # Hz
ada4522_noise_corner_freq = 0.1 # Hz

ada4898_input_voltage_noise = 0.9e-9 # V/sqrt(Hz)
ada4898_input_current_noise = 2.4e-12 # A/sqrt(Hz)
ada4898_GBW = 65e6 # Hz
ada4898_noise_corner_freq = 20 # Hz

ad8676_input_voltage_noise = 2.8e-9 # V/sqrt(Hz)
ad8676_input_current_noise = 0.3e-12 # A/sqrt(Hz)
ad8676_GBW = 10e6 # Hz
ad8676_noise_corner_freq = 30 # Hz

lt1206_input_voltage_noise = 3.6e-9 # V/sqrt(Hz)
lt1206_input_current_noise = 30e-12 # A/sqrt(Hz)
lt1206_GBW = 10e6 # Hz
lt1206_noise_corner_freq = 250 # Hz

ada4004_input_voltage_noise = 1.8e-9 # V/sqrt(Hz)
ada4004_input_current_noise = 1.2e-12 # A/sqrt(Hz)
ada4004_GBW = 12e6 # Hz
ada4004_noise_corner_freq = 10 # Hz

# Vref first stage ADA4522
vref_first_feedback_res = 5e3 # Ohms
vref_first_g_res = 5e3 # Ohms
vref_first_filter_res = 10e3 # Ohms
vref_first_filter_cap = 33e-6 # F
vref_first_gain = opn.inverting_opamp_gain(vref_first_feedback_res, vref_first_g_res)
vref_first_total_input_noise = opn.total_input_noise_rms(ada4522_input_voltage_noise, 
                                                            ada4522_input_current_noise, 
                                                            vref_first_feedback_res, 
                                                            vref_first_g_res, ada4522_GBW, 
                                                            filter_res=vref_first_filter_res, 
                                                            filter_cap=vref_first_filter_cap)
vref_first_total_output_noise = opn.total_output_noise_rms(vref_first_total_input_noise, 
                                                           vref_first_gain)
# print(f"vref_first total input noise: {vref_first_total_input_noise} Vrms")
print(f"vref_first total output noise: {vref_first_total_output_noise} Vrms")

# Vref second stage ADA4522
vref_second_feedback_res = 1e3 # Ohms
vref_second_g_res = 1e3 # Ohms
vref_second_filter_res = 1e3 # Ohms
vref_second_filter_cap = 4.7e-6 # F
vref_second_gain = opn.inverting_opamp_gain(vref_second_feedback_res, vref_second_g_res)
vref_second_total_input_noise = opn.total_input_noise_rms(ada4522_input_voltage_noise, 
                                                            ada4522_input_current_noise, 
                                                            vref_second_feedback_res, 
                                                            vref_second_g_res, ada4522_GBW, 
                                                            filter_res=vref_second_filter_res, 
                                                            filter_cap=vref_second_filter_cap)
vref_second_total_output_noise = opn.total_output_noise_rms(vref_second_total_input_noise, 
                                                            vref_second_gain)
# print(f"vref_second total input noise: {vref_second_total_input_noise} Vrms")
print(f"vref_second total output noise: {vref_second_total_output_noise} Vrms")

# Vref third stage ADA4898
vref_third_feedback_res = 5e3 # Ohms
vref_third_g_res = 1e3 # Ohms
vref_third_filter_res = 5e3 # Ohms
vref_third_filter_cap = 47e-6 # F
vref_third_gain = opn.inverting_opamp_gain(vref_third_feedback_res, vref_third_g_res)
vref_third_total_input_noise = opn.total_input_noise_rms(ada4898_input_voltage_noise, 
                                                            ada4898_input_current_noise, 
                                                            vref_third_feedback_res, 
                                                            vref_third_g_res, ada4898_GBW, 
                                                            filter_res=vref_third_filter_res, 
                                                            filter_cap=vref_third_filter_cap)
vref_third_total_output_noise = opn.total_output_noise_rms(vref_third_total_input_noise, 
                                                           vref_third_gain)
# print(f"vref_third total input noise: {vref_third_total_input_noise} Vrms")
print(f"vref_third total output noise: {vref_third_total_output_noise} Vrms")

# Vref buffer stage AD8676
vref_buffer_feedback_res = 1 # Ohms
vref_buffer_g_res = 1 # Ohms
vref_buffer_gain = opn.inverting_opamp_gain(vref_buffer_feedback_res, vref_buffer_g_res)
vref_buffer_total_input_noise = opn.total_input_noise_rms(ad8676_input_voltage_noise, 
                                                            ad8676_input_current_noise, 
                                                            vref_buffer_feedback_res, 
                                                            vref_buffer_g_res, ad8676_GBW, 
                                                            filter_res=None, 
                                                            filter_cap=None)
vref_buffer_total_output_noise = opn.total_output_noise_rms(vref_buffer_total_input_noise, 
                                                            vref_buffer_gain)
# print(f"vref_buffer total input noise: {vref_buffer_total_input_noise} Vrms")
print(f"vref_buffer total output noise: {vref_buffer_total_output_noise} Vrms")

total_vref_output_noise = (vref_first_total_output_noise + vref_second_total_output_noise
                           + vref_third_total_output_noise + vref_buffer_total_output_noise)
print(f"Total Vref output noise: {total_vref_output_noise} Vrms\n")

# Channel output
# First stage
dac_buffer_feedback_res = 1 # Ohms
dac_buffer_g_res = 1 # Ohms
dac_buffer_filter_res = 1e3 # Ohms
dac_buffer_filter_cap = 50e-6 # F
dac_buffer_gain = opn.inverting_opamp_gain(dac_buffer_feedback_res, dac_buffer_g_res)
dac_buffer_total_input_noise = opn.total_input_noise_rms(ada4522_input_voltage_noise, 
                                                            ada4522_input_current_noise, 
                                                            dac_buffer_feedback_res, 
                                                            dac_buffer_g_res, ada4522_GBW, 
                                                            filter_res=dac_buffer_filter_res, 
                                                            filter_cap=dac_buffer_filter_cap)
dac_buffer_total_output_noise = opn.total_output_noise_rms(dac_buffer_total_input_noise, dac_buffer_gain)
# print(f"dac_buffer total input noise: {dac_buffer_total_input_noise} Vrms")
print(f"dac_buffer total output noise: {dac_buffer_total_output_noise} Vrms")

# Second stage
feedback_driver_feedback_res = 1e3 # Ohms
feedback_driver_g_res = 1e3 # Ohms
feedback_driver_filter_res = 1e3 # Ohms, feedback res
feedback_driver_filter_cap = 10e-9 # F
feedback_driver_gain = opn.inverting_opamp_gain(feedback_driver_feedback_res, feedback_driver_g_res)
feedback_driver_total_input_noise = opn.total_input_noise_rms(ada4522_input_voltage_noise, 
                                                            ada4522_input_current_noise, 
                                                            feedback_driver_feedback_res, 
                                                            feedback_driver_g_res, ada4522_GBW, 
                                                            filter_res=feedback_driver_filter_res, 
                                                            filter_cap=feedback_driver_filter_cap)
feedback_driver_total_output_noise = opn.total_output_noise_rms(feedback_driver_total_input_noise, 
                                                                feedback_driver_gain)
# print(f"feedback_driver total input noise: {feedback_driver_total_input_noise} Vrms")
print(f"feedback_driver total output noise: {feedback_driver_total_output_noise} Vrms")

# Current driver stage
driver_feedback_res = 1e3 # Ohms
driver_g_res = 1e3 # Ohms
driver_filter_res = 1e3 # Ohms, feedback res
driver_filter_cap = 10e-9 # F
driver_gain = opn.inverting_opamp_gain(driver_feedback_res, driver_g_res)
driver_total_input_noise = opn.total_input_noise_rms(lt1206_input_voltage_noise, 
                                                            lt1206_input_current_noise, 
                                                            driver_feedback_res, 
                                                            driver_g_res, ada4522_GBW, 
                                                            filter_res=driver_filter_res, 
                                                            filter_cap=driver_filter_cap)
driver_total_output_noise = opn.total_output_noise_rms(driver_total_input_noise, driver_gain)
# print(f"driver total input noise: {driver_total_input_noise} Vrms")
print(f"driver total output noise: {driver_total_output_noise} Vrms")

# Current feedback stage
current_feedback_feedback_res = 2e3 # Ohms
current_feedback_g_res = 1e3 # Ohms
current_feedback_gain = opn.inverting_opamp_gain(current_feedback_feedback_res, current_feedback_g_res)
current_feedback_total_input_noise = opn.total_input_noise_rms(ada4522_input_voltage_noise, 
                                                            ada4522_input_current_noise, 
                                                            current_feedback_feedback_res, 
                                                            current_feedback_g_res, ada4522_GBW, 
                                                            filter_res=None, 
                                                            filter_cap=None)
current_feedback_total_output_noise = opn.total_output_noise_rms(current_feedback_total_input_noise, 
                                                                 current_feedback_gain)
# print(f"current feedback total input noise: {current_feedback_total_input_noise} Vrms")
print(f"current feedback total output noise: {current_feedback_total_output_noise} Vrms")

total_channel_output_noise = (dac_buffer_total_output_noise + feedback_driver_total_output_noise
                           + driver_total_output_noise + current_feedback_total_output_noise)
print(f"Total channel output noise: {total_channel_output_noise} Vrms\n")


# Grand total output noise
Rset = 10 # Ohms
Rload = 15 # Ohms
grand_total_output_noise = total_vref_output_noise + total_channel_output_noise
print(f"Grand total output noise: {grand_total_output_noise} Vrms")
print(f"Grand total current noise at 250 mA output: {grand_total_output_noise / (Rset + Rload)} Arms")

# Bar plot comparisions
x_names = ["Vref 1st", "Vref 2nd", "Vref 3rd", "Vref 4th", "DAC buffer", 
           "Channel control", "Driver", "Feedback"]
stages = np.array([vref_first_total_output_noise, vref_second_total_output_noise, 
              vref_third_total_output_noise, vref_buffer_total_output_noise,
              dac_buffer_total_output_noise, feedback_driver_total_output_noise,
              driver_total_output_noise, current_feedback_total_output_noise])
stages_micro_volt_rms = stages / 1e-6

# Newest design (with ADA4004 in DAC buffer and feedback loop)
new_dac_buffer_total_input_noise = opn.total_input_noise_rms(ada4004_input_voltage_noise, 
                                                            ada4004_input_current_noise, 
                                                            dac_buffer_feedback_res, 
                                                            dac_buffer_g_res, ada4004_GBW, 
                                                            filter_res=dac_buffer_filter_res, 
                                                            filter_cap=dac_buffer_filter_cap)
new_dac_buffer_total_output_noise = opn.total_output_noise_rms(new_dac_buffer_total_input_noise, 
                                                               dac_buffer_gain)

new_feedback_driver_total_input_noise = opn.total_input_noise_rms(ada4004_input_voltage_noise, 
                                                            ada4004_input_current_noise, 
                                                            feedback_driver_feedback_res, 
                                                            feedback_driver_g_res, ada4004_GBW, 
                                                            filter_res=feedback_driver_filter_res, 
                                                            filter_cap=feedback_driver_filter_cap)
new_feedback_driver_total_output_noise = opn.total_output_noise_rms(new_feedback_driver_total_input_noise, 
                                                                feedback_driver_gain)

new_current_feedback_total_input_noise = opn.total_input_noise_rms(ada4004_input_voltage_noise, 
                                                            ada4004_input_current_noise, 
                                                            current_feedback_feedback_res, 
                                                            current_feedback_g_res, ada4004_GBW, 
                                                            filter_res=None, 
                                                            filter_cap=None)
new_current_feedback_total_output_noise = opn.total_output_noise_rms(new_current_feedback_total_input_noise, 
                                                                 current_feedback_gain)

new_stages = np.array([vref_first_total_output_noise, vref_second_total_output_noise, 
              vref_third_total_output_noise, vref_buffer_total_output_noise,
              new_dac_buffer_total_output_noise, new_feedback_driver_total_output_noise,
              driver_total_output_noise, new_current_feedback_total_output_noise])
new_stages_micro_volt_rms = new_stages / 1e-6 # Convert from Vrms to microVrms
new_stages_total = np.sum(new_stages)
old_stages_total = np.sum(stages) 

# print(f"old: {stages_micro_volt_rms} uVrms")
# print(f"new: {new_stages_micro_volt_rms} uVrms/n")
print(f"Grand total output noise old: {old_stages_total / 1e-6} uVrms")
print(f"Grand total output noise new: {new_stages_total / 1e-6} uVrms")

plt.bar(x_names,new_stages_micro_volt_rms, color='r', label='with ADA4004')
plt.bar(x_names,stages_micro_volt_rms, color='b', alpha=0.5, label='with ADA4522')
plt.xticks(rotation=90)
plt.legend()
plt.xlabel("Stages")
plt.ylabel("uVrms")
plt.title("Evan Noise Contributions")
plt.tight_layout()
plt.show()