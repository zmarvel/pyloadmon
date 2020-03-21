

from dataclasses import dataclass
import dataclasses
from enum import Enum
from pathlib import Path
import os


class State(Enum):
    RUNNING = 'R'
    SLEEPING = 'S'
    WAITING_DISK = 'D'
    ZOMBIE = 'Z'
    STOPPED = 'T'
    TRACING_STOP = 't'
    DEAD = 'X'
    WAKEKILL = 'K'
    WAKING = 'W'
    PARKED = 'P'
    # Not in Debian 10 proc(5)
    IDLE = 'I'


class SchedPolicy(Enum):
    NORMAL = 0
    FIFO = 1
    RR = 2
    BATCH = 3
    ISO = 4
    IDLE = 5
    DEADLINE = 6


@dataclass
class Status:
    state: State = State.ZOMBIE
    parent_pid: int = 0
    utime: int = 0
    stime: int = 0
    priority: int = 0
    num_threads: int = 0
    text_size: int = 0
    rss: int = 0
    vsize: int = 0
    shared_size: int = 0
    data_size: int = 0
    processor: int = 0
    policy: SchedPolicy = SchedPolicy.NORMAL

    def asdict(self):
        return dataclasses.asdict(self)

class Proc:
    page_size = 0

    def __init__(self, pid):
        self.pid = pid
        self.proc_dir = Path('/proc', str(self.pid))
        if self.page_size == 0:
            try:
                self.page_size = self._read_page_size()
            except PermissionError:
                pass
        # self.cmdline = self._read_command_line()
        self.cmdline = self._read_command_line(1)
        self.status = Status()

    @property
    def present(self):
        return self.proc_dir.exists()

    def sample(self):
        self._read_stat()
        return self.status

    def _read_stat(self):
        with open(self.proc_dir / 'stat', 'r') as f:
            line = f.read().rstrip()
            parts = line.split(' ')
            for i, part in enumerate(parts):
                if ')' in part and '(' not in part:
                    break
            del parts[i]

        clk_tck = os.sysconf('SC_CLK_TCK')
        def ticks(s: str) -> int:
            return int(s) / clk_tck

        def pages_to_bytes(s: str) -> int:
            return int(s) * self.page_size

        def update_col(attr, col, type):
            setattr(self.status, attr, type(parts[col]))

        update_col('state', 2, State)
        update_col('parent_pid', 3, int)
        update_col('utime', 13, ticks)
        update_col('stime', 14, ticks)
        update_col('priority', 17, int)
        update_col('num_threads', 19, int)
        update_col('vsize', 22, pages_to_bytes)
        update_col('rss', 23, pages_to_bytes)
        update_col('processor', 38, int)
        update_col('policy', 40, int)

    def _read_statm(self):
        pass

    def _read_page_size(self):
        # only needs to be called once and can be determined from
        # `/proc/pid/smaps`
        smaps_path = self.proc_dir / 'smaps'
        MAX_LINES = 32
        page_size_kb = None
        with open(smaps_path, 'r') as f:
            for i in range(MAX_LINES):
                line = f.readline()
                if 'KernelPageSize' in line:
                    page_size_kb = line.split(':')[1].strip()
                    break
        if page_size_kb is not None:
            return int(page_size_kb.split(' ')[0]) * 1024
        else:
            return 0

    def _read_command_line(self, n=-1):
        # only needs to be called once--`/proc/pid/cmdline`
        cmdline_path = self.proc_dir / 'cmdline'
        with open(cmdline_path, 'rb') as f:
            line = f.read()
            parts = line.split(b'\0')
            parts[-1].rstrip()
            return ' '.join([p.decode('utf8') for p in parts[:n]])
