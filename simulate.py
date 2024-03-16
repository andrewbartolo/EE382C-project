#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor as ThreadPool

BOOKSIM_EXE = './booksim2/src/booksim'
BASE_CFG = './base.cfg'
OUT_DIR = './sim-out'
N_WORKER_THREADS = 24

def run_cmd(booksim_exe, base_cfg, out_dir, k, packet_size, traffic, routing, rate):
    prefix = Path(out_dir, f'K{k}-S{packet_size}-T{traffic}-R{routing}-I{int(rate*100):03d}')
    print(f"launching {prefix}...")

    m_path = prefix.with_suffix('.m')
    stdout_path = prefix.with_suffix('.out')

    # run the command, making the necessary variable subsitutions from base config
    res = subprocess.run([booksim_exe, base_cfg,
                          f'k={k}',
                          f'packet_size={packet_size}',
                          f'traffic={traffic}',
                          f'routing_function={routing}',
                          f'injection_rate={rate}',
                          f'stats_out={m_path}'],
                          stdout=subprocess.PIPE, text=True)
    # save captured stdout to file
    with open(stdout_path, 'w') as f:
        f.write(res.stdout)

    print(f"    completed {prefix}.")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    tp = ThreadPool(max_workers=N_WORKER_THREADS)

    # sweep over the following parameters
    for k in [4, 8]:
        for packet_size in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
            # tornado exhibited some weird results; stick with 'uniform' and 'neighbor' for now
            for traffic in ['allreduce', 'neighbor', 'uniform']:
                for routing in ['dor', 'min_adapt', 'xy_yx']:
                    for rate in [x/100 for x in range(5, 100, 5)]:
                        # NOTE: all submitted threads will implicitly be joined before the program exits
                        # (https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor)
                        tp.submit(run_cmd, BOOKSIM_EXE, BASE_CFG, OUT_DIR, k, packet_size, traffic,
                                  routing, rate)


if __name__ == '__main__':
    main()
