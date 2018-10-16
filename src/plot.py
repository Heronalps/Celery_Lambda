import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
from statistics import stdev

def plot_curve(field):
    x_point = []
    y_point = []
    for num in range(6, 48, 6):
        path = str("../result/metrics_CA%dLA_20181015.data" %num)
        data = []
        with open(path, 'r') as f:
            line = f.readline()
            while line:
                hash = json.loads(line)
                data.append(hash[field]/1000)
                line = f.readline()
        y_point.append(mean(data))
        x_point.append(num)

    print(x_point)
    print(y_point)

    _fig, _ax = plt.subplots()    
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Experiment Number')
    plt.ylabel('Total Billed Duration (seconds)')
    plt.title('Centaurus Metrics', fontsize=10)
    plt.plot(x_point, y_point, 'bo-')
    plt.show()
    

def plot_hist(path, field):
    data = []
    with open(path, "r") as f:
        line = f.readline()
        while line:
            hash = json.loads(line)
            data.append(hash[field])
            line = f.readline()

    sample_size = len(data)
    mean_data = round(mean(data), 3)
    std_data = round(std(data), 3)
    # Introduce confidence interval to toss outliners
    upper_bound = mean_data + std_data * 3
    lower_bound = mean_data - std_data * 3
    for d in data:
        if (d >= upper_bound or d <= lower_bound):
            data.remove(d)

    max_data = round(max(data), 3)
    min_data = round(min(data), 3)
    
    metrics = "sample size = " + str(sample_size) + \
              ", max = " + str(max_data) + \
              ", min = " + str(min_data) + \
              r'$,\ \mu = ' + str(mean_data) + \
              r',\ \sigma = $' + str(std_data)
    # print(metrics)
    # An "interface" to matplotlib.axes.Axes.hist() method

    _fig, ax = plt.subplots()

    _n, _bins, _patches = ax.hist(x=data, bins=int(sample_size/2), color='#0504aa',
                                alpha=0.7, rwidth=0.85, histtype="bar", density=True, 
                                label="PDF")

    _n, _bins, _patches = ax.hist(x=data, bins=int(sample_size/2), color='#0932ba',
                                alpha=0.7, rwidth=0.85, histtype="step", cumulative=True, 
                                label="empirical CDF", density=True)
    
    norm_dist_y = np.random.normal(mean_data, std_data, sample_size)
    
    _n, _bins, _patches = ax.hist(x=norm_dist_y, bins=int(sample_size/2), color='#FF5733',
                                alpha=0.7, rwidth=0.85, histtype="step", cumulative=True, 
                                label="artificial CDF", density=True)
    
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Total Duration (millisec)')
    plt.ylabel('Probability Density')
    ax.legend(loc='upper left')
    plt.title('Histogram - Sync Celery, Sync Lambda, Invocation = 100\n' + metrics, fontsize=10)
    
    # maxfreq = n.max()
    # Set a clean upper y-axis limit.
    # plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    
    plt.xlim(0,400)
    
    plt.show() 

def mean(data):
    return float(sum(data) / len(data))

def std(data):
    return stdev(data)

# All plotable fields
# "total_duration"
# "total_billed_duration" 
# "max_memory_used" 
# "memory_size" 
# "duration_per_invocation" 
# "compute_charge" 
# "cost" 
# 'host_execu_time'

if __name__ == '__main__':
    plot_curve('total_duration')
