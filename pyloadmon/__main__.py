
import dataclasses
from time import sleep

from tabulate import tabulate

from pyloadmon.sampler import Sampler

def main():
    # sort by pid for now

    sampler = Sampler()
    while True:
        status = sampler.sample()
        table = []
        for pid, st in status.items():
            st = dataclasses.asdict(st)
            st['pid'] = pid
            st['cmdline'] = sampler.get_cmdline(pid)
            table.append(st)
        table.sort(key=lambda st: st['pid'])
        print(tabulate(table, headers='keys'))
        print()
        sleep(1)

if __name__ == '__main__':
    main()
