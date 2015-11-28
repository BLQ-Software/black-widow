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

        fig = plt.figure(1, figsize=(15,8))

        fig.suptitle(case_num, fontsize=32, fontweight='bold')

    

if __name__ == '__main__':
    data_dir = '../../data'
    log_files = ['case0', 'case1', 'case2']
    
    for log_file in log_files:
    
        smooth_factor = 100

        devices = [['F1', 'flow', 1], ['F2', 'flow', 1], ['F3', 'flow', 1], ['L1', 'link', 2]]
        data_types = ['sent', 'received']
     
        flow_path = '{}/{}.{}_{}.{}.csv'
        
        fig = plt.figure(1, figsize=(15,8))
        fig.suptitle(log_file, fontsize=32, fontweight='bold')

        for i, device in enumerate(devices):
            for j, data_type in enumerate(data_types):
                file_name = flow_path.format(data_dir, log_file, device[1], device[0], data_type)

                if (os.path.isfile(file_name)):
                    print 'Graphing {} {}'.format(device[0], data_type)
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
                    
                    if delta_t != 0:
                        rate.append(sum_data / delta_t / 1000.0)
                        time.append(sum_time / float(smooth_factor))

                plt.subplot(5, 1, devices[i][2])
                plt.plot(time, rate)
                plt.xlabel('time (ms)')
                plt.ylabel('{} {} rate (Mbps)'.format(device[0], data_type))
                plt.draw()
        
        plt.show()
            
        


