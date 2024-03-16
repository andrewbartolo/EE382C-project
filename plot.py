#!/usr/bin/env python3
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

CSV_FILE = './data.csv'
TRAFFIC_PATTERN = 'uniform'
ROUTING = 'dor'
LAT_OR_HOPS = 0    # choose one of these to plot. lat: 0; hops: 1
PROPERTY = ['avg_lat', 'avg_hops'][LAT_OR_HOPS]
Y_LABEL = ['Average packet latency (cycles)', 'Average hop count'][LAT_OR_HOPS]
X_LABEL = 'Flit injection rate'

# returns a list of (x, y) tuples where x: injection rate, and y: latency
def get_points(key, traffic, routing, k, packet_size):
    # do a full separate pass through the file for each set of points
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        return [(float(row['rate']), float(row[key])) for row in reader \
            if (
                row['traffic'] == traffic and \
                row['routing'] == routing and \
                int(row['k']) == k and \
                int(row['packet_size']) == packet_size and \
                # NaN check
                not math.isnan(float(row[key]))
            )]

# make some plots for TRAFFIC_PATTERN traffic
# NOTE: easier to define packet_sizes in terms of explicit multipliers
multipliers = [1, 8, 64, 512]

data = {}
for k in [4, 8]:
    data[k] = {}
    # final element is the "multiplier" used for comparison to M3D
    # (lower packet sizes correspond to *higher* channel bandwidth)
    for multiplier in multipliers:
        packet_size = multipliers[-1] / multiplier
        data[k][multiplier] = get_points(PROPERTY, TRAFFIC_PATTERN, ROUTING, k, packet_size)


fig, ax = plt.subplots()

for k in [4, 8]:
    line_type = '--' if k == 4 else '-'
    for multiplier in multipliers:
        print(data)
        points = data[k][multiplier]
        x, y = list(zip(*points))
        plt.plot(x, y, line_type, label=f'k={k}; {multiplier}X BW')

ax.set_xlabel(X_LABEL, fontsize=13)
ax.set_ylabel(Y_LABEL, fontsize=13)
ax.tick_params(axis='x', labelsize=13)
ax.tick_params(axis='y', labelsize=13)
ax.legend(ncol=2, fontsize=13)

# reduce margins
fig.tight_layout()


output_dir = 'render'
os.makedirs(output_dir, exist_ok=True)

plt.savefig(f'{output_dir}/{PROPERTY}-{TRAFFIC_PATTERN}-{ROUTING}.pdf')
plt.savefig(f'{output_dir}/{PROPERTY}-{TRAFFIC_PATTERN}-{ROUTING}.png', dpi=600)
plt.savefig(f'{output_dir}/{PROPERTY}-{TRAFFIC_PATTERN}-{ROUTING}.svg', transparent=True)

plt.close()
