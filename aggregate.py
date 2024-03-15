#!/usr/bin/env python3
import csv
import os
from pathlib import Path

SIM_OUT_DIR = './sim-out'
CSV_OUT = 'data.csv'

def foo():
    pass

    '''
    res = subprocess.run(["./booksim", "base.cfg"], stdout=subprocess.PIPE, text=True)
    #print(res.stdout)

    # TODO parser
    lines = res.stdout.split('\n')
    start_idx = [i for (i, line) in enumerate(lines) if 'Overall Traffic Statistics' in line][0]

    print(lines[start_idx:])
    '''

# return a 2-tuple of (avg_lat, avg_hops)
def read_file(sim_out_dir, k, packet_size, traffic, rate):
    prefix = Path(sim_out_dir, f'K{k}-S{packet_size}-T{traffic}-R{int(rate*100):03d}')
    stdout_path = prefix.with_suffix('.out')

    with open(stdout_path, 'r') as f:
        lines = f.readlines()

    # check if simulation was unstable; if so, record a NaN for latency
    if 'unstable' in lines[-2]: return (float('NaN'), float('NaN'))

    summary_start_idx = \
            [i for (i, line) in enumerate(lines) if 'Overall Traffic Statistics' in line][0]
    summary_lines = lines[summary_start_idx:]

    # average latency is in the summary section line 2, column 4
    avg_lat = float(summary_lines[2].split()[4])
    avg_hops = float(summary_lines[28].split()[3])
    return (avg_lat, avg_hops)


def main():
    assert(os.path.isdir(SIM_OUT_DIR))

    csv_file = open(CSV_OUT, 'w', newline='')
    fieldnames = ['k', 'packet_size', 'traffic', 'rate', 'avg_lat', 'avg_hops']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # sweep over the following parameters
    for traffic in ['uniform', 'neighbor', 'allreduce']:
        for k in [4, 8]:
            for packet_size in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
                for rate in [x/100 for x in range(5, 100, 5)]:
                    file_data = read_file(SIM_OUT_DIR, k, packet_size, traffic, rate)
                    writer.writerow({'k': k,
                                     'packet_size': packet_size,
                                     'traffic': traffic,
                                     'rate': rate,
                                     'avg_lat': file_data[0],
                                     'avg_hops': file_data[1]})

    csv_file.close()

if __name__ == '__main__':
    main()
