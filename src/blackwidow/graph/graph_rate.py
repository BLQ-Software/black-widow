import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class GraphSettings(object):
    """Emulates bw object if run from script."""
    def __init__(self, data_dir, log_file):
        self.data_dir = data_dir
        self.log_file = log_file

class CsvGrapher(object):
    """Graphs the .csv files."""
    
    def __init__(self, num_graphs, bw):
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
        sns.set()
        case_num = self.bw.log_file
        cc_type = 'Fixed Window'

        self.fig = plt.figure(1, figsize=(15,8))

        self.fig.suptitle(case_num, fontsize=32, fontweight='bold')

    

if __name__ == '__main__':
    data_dir = '../../data'
    log_files = ['case0', 'case1', 'case2']
    
    smooth_factor = 100
    max_capacity = 12.5  # Used to remove outliers in calculations. 
    
    for log_file in log_files:
    
        devices = [['F1', 'flow', 1], ['F2', 'flow', 1], ['F3', 'flow', 1], 
                   ['L1', 'link', 2], ['L2', 'link', 2], ['L3', 'link', 2]]
        
        data_types = ['sent', 'received']
     
        flow_path = '{}/{}.{}_{}.{}.csv'
        
        fig = plt.figure(1, figsize=(15,8))
        fig.suptitle(log_file, fontsize=32, fontweight='bold')

        # Keep track of maximum subplot number seen so far.
        max_subplot_no = 1 

        # Rate calculations.
        for i, device in enumerate(devices):
            for j, data_type in enumerate(data_types):
                file_name = flow_path.format(data_dir, log_file, device[1], device[0], data_type)

                if (os.path.isfile(file_name)):
                    print 'Computing {} {} {}'.format(log_file, device[0], data_type)
                else:    
                    continue

                data = np.genfromtxt(file_name, delimiter=',')
                rate = []
                time = []
                for k in range(data.size / 2 - smooth_factor):
                    sum_data = 0
                    sum_time = 0
                    for n in range(smooth_factor):
                        sum_data += data[k + n][1]
                        sum_time += data[k + n][0]

                    delta_t = data[k + smooth_factor - 1][0] - data[k][0]
                    new_rate = sum_data / delta_t / 1000.0
                    
                    if delta_t != 0 and new_rate <= 12.5:
                        rate.append(new_rate)
                        time.append(sum_time / float(smooth_factor))

                subplot_no = device[2] * len(data_types) + j
                max_subplot_no = max(subplot_no, max_subplot_no)
                plt.subplot(5, 1, subplot_no)
                plt.plot(time, rate, label=device[0])
                plt.legend()
                plt.xlabel('time (ms)')
                plt.ylabel('{} {} rate (Mbps)'.format(device[1], data_type))
                plt.draw()
        
        fig.tight_layout()
        plt.show()

        
        # Create the paths to the data files
        link_rate_path = '{}/{}.link_L1.rate.csv'.format(data_dir, log_file)
        buffer_occupancy_path = '{}/{}.link_L1.buffer.csv'.format(data_dir, log_file)
        packet_loss_path = '{}/{}.link_L1.drop.csv'.format(data_dir, log_file)
        window_size_path = '{}/{}.flow_F1.window.csv'.format(data_dir, log_file)
        packet_sent_path = '{}/{}.link_L1.sent.csv'.format(data_dir, log_file)


        # PLOTTING GRAPHS


        # LOADING DATA
        if (os.path.isfile(buffer_occupancy_path)):
            # Load in buffer occupancy data
            buffer_occupancy = np.genfromtxt(buffer_occupancy_path, delimiter=',')
            buffer_occupancy = buffer_occupancy.astype(int)
            buffer_occupancy_times = buffer_occupancy[:,0]
            buffer_occupancy = buffer_occupancy[:,1]

            # Plot the buffer occupancy
            plt.subplot(2, 1, 1)
            plt.plot(buffer_occupancy_times, buffer_occupancy)
            plt.xlabel('time (ms)')
            plt.ylabel('buffer occupancy (pkts)')

        if (os.path.isfile(window_size_path)):
            # Load in window size data
            window_size = np.genfromtxt(window_size_path, delimiter=',')
            window_size = window_size.astype(int)
            window_size_times = window_size[:,0]
            window_size = window_size[:,1]

            # Plot the window size
            plt.subplot(2, 1, 2)
            plt.plot(window_size_times, window_size, markersize=5)
            plt.xlabel('time (ms)')
            plt.ylabel('window size (pkts)')

        
        fig.tight_layout()
        plt.show()
            
        


