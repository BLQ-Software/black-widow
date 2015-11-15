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
   
# Determine the x-axis
sim_time = 30000 
t = np.arange(sim_time)
 

# Create the paths to the data files
### TO BE MODIFIED: for each type of data, choose the most recent date
link_rate_path = '../../data/case0_11-13-2015_20:51.link_L1.rate.csv'
buffer_occupancy_path = '../../data/case0_11-13-2015_20:51.link_L1.buffer.csv'
packet_loss_path = '../../data/case0_11-13-2015_20:51.link_L1.drop.csv'
window_size_path = '../../data/case0_11-13-2015_20:51.flowF1.window.csv'


# LOADING DATA

# Load in link rate data
link_rate = np.genfromtxt(link_rate_path, delimiter=',')
link_rate = link_rate.astype(int)
link_rate_times = link_rate[:,0]
link_rate = link_rate[:,1]

# Load in buffer occupancy data
buffer_occupancy = np.genfromtxt(buffer_occupancy_path, delimiter=',')
buffer_occupancy = buffer_occupancy.astype(int)
buffer_occupancy_times = buffer_occupancy[:,0]
buffer_occupancy = buffer_occupancy[:,1]

# Load in packet loss data
packet_loss_times = np.genfromtxt(packet_loss_path)
packet_loss_times = packet_loss_times.astype(int)
packet_loss = np.zeros(sim_time)

for x in np.nditer(packet_loss_times):
    packet_loss[x] = packet_loss[x] + 1

# Load in window size data
window_size = np.genfromtxt(window_size_path, delimiter=',')
window_size = window_size.astype(int)
window_size_times = window_size[:,0]
window_size = window_size[:,1]

# Load in packet sent data



# PLOTTING GRAPHS
plt.figure(1)

# Plot the link rate
plt.subplot(4, 1, 1)
plt.plot(link_rate_times, link_rate, markersize=5)
plt.xlabel('time (ms)')
plt.ylabel('link rate (Mbps)')

# Plot the buffer occupancy
plt.subplot(4, 1, 2)
plt.plot(buffer_occupancy_times, buffer_occupancy)
plt.xlabel('time (ms)')
plt.ylabel('buffer occupancy (pkts)')

# Plot the packet loss
plt.subplot(4, 1, 3)
plt.plot(t, packet_loss, markersize=5)
plt.xlabel('time (ms)')
plt.ylabel('packet loss (pkts)')

# Plot the window size
plt.subplot(4, 1, 4)
plt.plot(window_size_times, window_size, markersize=5)
plt.xlabel('time (ms)')
plt.ylabel('window size (pkts)')




