# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 23:11:24 2015

@author: nancywen
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Grapher(object):
    """Graphing class for blackwidow."""

    def __init__(self, bw):
        """Constructor for graph object."""
        self.bw = bw
        self.data_dir = bw.data_dir
        self.log_file = bw.log_file
        
    def graph(self, sim_time):
        """Graphs the simulation."""
        sns.set()

        case_num = self.bw.log_file
        cc_type = 'Fixed Window'
           
        # Determine the x-axis
        t = np.arange(sim_time)
         


        # Create the paths to the data files
        ### TO BE MODIFIED: for each type of data, choose the most recent date
        link_rate_path = '{}/{}.link_L1.rate.csv'.format(self.data_dir, self.log_file)
        buffer_occupancy_path = '{}/{}.link_L1.buffer.csv'.format(self.data_dir, self.log_file)
        packet_loss_path = '{}/{}.link_L1.drop.csv'.format(self.data_dir, self.log_file)
        window_size_path = '{}/{}.flow_F1.window.csv'.format(self.data_dir, self.log_file)
        packet_sent_path = '{}/{}.link_L1.sent.csv'.format(self.data_dir, self.log_file)


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
        packet_sent = np.genfromtxt(packet_sent_path, delimiter=',')
        packet_sent = packet_sent.astype(int)
        packet_sent_times = packet_sent[:,0]
        packet_sent = packet_sent[:,1]

        # PLOTTING GRAPHS
        fig = plt.figure(1)
        fig.suptitle(case_num, fontsize=14, fontweight='bold')

        # Plot the link rate
        plt.subplot(5, 1, 1)
        plt.plot(link_rate_times[::2], link_rate[::2], markersize=5)
        plt.xlabel('time (ms)')
        plt.ylabel('link rate (Mbps)')

        # Plot the buffer occupancy
        plt.subplot(5, 1, 2)
        plt.plot(buffer_occupancy_times, buffer_occupancy)
        plt.xlabel('time (ms)')
        plt.ylabel('buffer occupancy (pkts)')

        # Plot the packet loss
        plt.subplot(5, 1, 3)
        plt.plot(t, packet_loss, markersize=5)
        plt.xlabel('time (ms)')
        plt.ylabel('packet loss (pkts)')

        # Plot the window size
        plt.subplot(5, 1, 4)
        plt.plot(window_size_times, window_size, markersize=5)
        plt.xlabel('time (ms)')
        plt.ylabel('window size (pkts)')

        # Plot the packets send
        plt.subplot(5, 1, 5)
        plt.plot(packet_sent_times, packet_sent)
        plt.xlabel('time (ms)')
        plt.ylabel('packets sent (pkts)')

        plt.show()
