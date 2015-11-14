# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 23:11:24 2015

@author: nancywen
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

case_num = 'Case 0'
cc_type = 'Fixed Window'
   


# Create the paths to the data files
packet_loss_path = '../data/case0_11-12-2015_21_14.link_L1.drop.csv'
window_size_path = '../data/case0_11-12-2015_21_14.flowF1.window.csv'

# Load in data
packet_loss_times = np.genfromtxt(packet_loss_path)
packet_loss_times = packet_loss_times.astype(int)
packet_loss = np.zeros(sim_time)

for x in np.nditer(packet_loss_times):
    packet_loss[x] = packet_loss[x] + 1


window_size = np.genfromtxt(window_size_path, delimiter=',')
window_size = window_size.astype(int)

window_size_times = window_size[:,0]
window_size = window_size[:,1]

plt.plot(window_size_times, window_size)


"""
# Determine the x-axis
sim_time = 30000 
t = np.arange(sim_time)
 
# Plot the packet loss
plt.plot(t, packet_loss, markersize=5)
plt.title('Packet loss over time')
plt.xlabel('Time (ms)')
plt.ylabel('Packet loss (pkts)')



"""