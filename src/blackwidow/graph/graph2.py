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
packet_loss_path = '../data/case0.link_L1.drop.csv'

#window_size_path = '../data/case0.window.csv'
    
    # Load in the data
    ### link_rate = np.loadtxt(link_rate_path)
    ### buffer_occupancy = np.loadtxt(buffer_occupancy_path)
packet_loss = np.genfromtxt(packet_loss_path)
    ### flow_rate = np.loadtxt(flow_rate_path)
###window_size = np.loadtxt(window_size_path)
    ### packet_delay = np.loadtxt(packet_delay_path)

# Packet loss    
t = np.arange(0, packet_loss.shape[0])
plt.plot(t, packet_loss, marker='.', linestyle='', markersize=10)
plt.title('Packet loss over time')
plt.xlabel('Time (s)')
plt.ylabel('Packet loss (pkts)')
#plt.legend(('Link 1'), loc='upper left')

#


    #Generate a time series for the packet loss

