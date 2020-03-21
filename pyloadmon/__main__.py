
from time import sleep

from tabulate import tabulate

from pyloadmon.sampler import Sampler

def main():
    # sort by pid for now

    sampler = Sampler()
    while True:
        status = sampler.sample()
        status.sort(key=lambda st: st['pid'])
        print(tabulate(status, headers='keys'))
        print()
        sleep(1)

if __name__ == '__main__':
    main()
