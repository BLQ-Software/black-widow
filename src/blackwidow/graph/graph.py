# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 23:11:24 2015

@author: nancywen
"""
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

import pyqtgraph as pg
import numpy as np
pg.mkQApp()

import pyqtgraph.multiprocess as mp
proc = mp.QtProcess()
rpg = proc._import('pyqtgraph')
plotwin = rpg.plot()
curve = plotwin.plot(pen='y')

x_data = proc.transfer([])
data = proc.transfer([])

# plt.ion()

class Grapher(object):
    """Graphing class for blackwidow."""

    def __init__(self, num_graphs, bw, queue = None):
        """Constructor for graph object."""
        self.bw = bw
        self.data_dir = bw.data_dir
        self.log_file = bw.log_file
        self.subplot_id = 1
        self.data_type_ids = {}
        self.data_type_data = {}
        self.num_graphs = num_graphs
        self.subplots = {}
        self.num_points = 0
        self.queue = queue
        sns.set()

        # Determine the x-axis

    def plot_link(self, x, y):
        x_data.extend([x], _callSync='off')
        data.extend([y], _callSync='off')
        curve.setData(x=x_data, y=data, _callSync='off')

    def init_plot(self, data_type, xlabel, ylabel):
        self.subplots[data_type] = plt.subplot(self.num_graphs, 1, self.subplot_id)
        self.subplots[data_type].set_xlabel(xlabel)
        self.subplots[data_type].set_ylabel(ylabel)

    def plot(self, data, data_type, xlabel, ylabel):

        if len(data) == 1:
            data = (data[0], 1)

        if data_type in self.data_type_ids:
            subplot_id = self.data_type_ids[data_type]
        else:
            subplot_id = 1
            self.data_type_ids[data_type] = self.subplot_id
            self.data_type_data[data_type] = ([], [])
            self.init_plot(data_type, xlabel, ylabel)
            self.subplot_id += 1
        self.data_type_data[data_type][0].append(data[0])
        self.data_type_data[data_type][1].append(data[1])

        self.subplots[data_type].plot(self.data_type_data[data_type][0], self.data_type_data[data_type][1], 'or')
        self.num_points += 1
        if (self.num_points % 100 == 0):
            plt.draw()
            plt.show()


    def graph(self, sim_time):
        """Graphs the simulation."""

        case_num = self.bw.log_file
        cc_type = 'Fixed Window'

        fig = plt.figure(1, figsize=(15,8))

        fig.suptitle(case_num, fontsize=14, fontweight='bold')

        t = np.arange(sim_time)

        # Create the paths to the data files
        link_rate_path = '{}/{}.link_L1.rate.csv'.format(self.data_dir, self.log_file)
        buffer_occupancy_path = '{}/{}.link_L1.buffer.csv'.format(self.data_dir, self.log_file)
        packet_loss_path = '{}/{}.link_L1.drop.csv'.format(self.data_dir, self.log_file)
        window_size_path = '{}/{}.flow_F1.window.csv'.format(self.data_dir, self.log_file)
        packet_sent_path = '{}/{}.link_L1.sent.csv'.format(self.data_dir, self.log_file)


        # PLOTTING GRAPHS


        # LOADING DATA

        if (os.path.isfile(link_rate_path)):
            # Load in link rate data
            link_rate = np.genfromtxt(link_rate_path, delimiter=',')
            link_rate = link_rate.astype(float)
            link_rate = bin(link_rate, 100)

            link_rate_times = link_rate[:,0]
            link_rate = link_rate[:,1]

            # Plot the link rate
            plt.subplot(5, 1, 1)
            plt.plot(link_rate_times[::2], link_rate[::2], markersize=5)
            plt.xlabel('time (ms)')
            plt.ylabel('link rate (Mbps)')

        if (os.path.isfile(buffer_occupancy_path)):
            # Load in buffer occupancy data
            buffer_occupancy = np.genfromtxt(buffer_occupancy_path, delimiter=',')
            buffer_occupancy = buffer_occupancy.astype(int)
            buffer_occupancy_times = buffer_occupancy[:,0]
            buffer_occupancy = buffer_occupancy[:,1]

            # Plot the buffer occupancy
            plt.subplot(5, 1, 2)
            plt.plot(buffer_occupancy_times, buffer_occupancy)
            plt.xlabel('time (ms)')
            plt.ylabel('buffer occupancy (pkts)')

        if (os.path.isfile(packet_loss_path)):
            # Load in packet loss data
            packet_loss_times = np.genfromtxt(packet_loss_path)
            packet_loss_times = packet_loss_times.astype(int)
            packet_loss = np.zeros(sim_time)

            for x in np.nditer(packet_loss_times):
                packet_loss[x] = packet_loss[x] + 1

            # Plot the packet loss
            plt.subplot(5, 1, 3)
            plt.plot(t, packet_loss, markersize=5)
            plt.xlabel('time (ms)')
            plt.ylabel('packet loss (pkts)')

        if (os.path.isfile(window_size_path)):
            # Load in window size data
            window_size = np.genfromtxt(window_size_path, delimiter=',')
            window_size = window_size.astype(int)
            window_size_times = window_size[:,0]
            window_size = window_size[:,1]

            # Plot the window size
            plt.subplot(5, 1, 4)
            plt.plot(window_size_times, window_size, markersize=5)
            plt.xlabel('time (ms)')
            plt.ylabel('window size (pkts)')

        if (os.path.isfile(packet_sent_path)):
            # Load in packet sent data
            packet_sent = np.genfromtxt(packet_sent_path, delimiter=',')
            packet_sent = packet_sent.astype(int)
            packet_sent_times = packet_sent[:,0]
            packet_sent = packet_sent[:,1]

            # Plot the packets send
            plt.subplot(5, 1, 5)
            plt.plot(packet_sent_times, packet_sent)
            plt.xlabel('time (ms)')
            plt.ylabel('packets sent (pkts)')
        plt.draw()
        plt.show()

def bin(data, time=1000):
    data_time = []
    data_n = []

    previous_time = 0
    sum = 0
    count = 0

    for i in range(0, data.shape[0]):
        time_n = int(data[i][0] / time) * time
        if (i == 0):
            previous_time = time_n
        if time_n == previous_time:
            sum += data[i][1]
            count += 1
        else:
            data_time.append(previous_time)
            data_n.append(float(sum) / float(count))
            previous_time = time_n
            sum = data[i][1]
            count = 1
    data_time.append(previous_time)
    data_n.append(float(sum) / float(count))
    return np.array([data_time, data_n]).transpose()
