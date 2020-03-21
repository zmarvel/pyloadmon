
from typing import List, Dict, TYPE_CHECKING
import glob
from pathlib import Path

from pyloadmon.procfs import Proc

if TYPE_CHECKING:
    from pyloadmon.procfs import Status


class Sampler:
    def __init__(self, pids: List[int] = None):
        self.pids: List[int] = pids
        self.proc: Dict[int, Proc] = {}
        self.status: List[dict] = []

    def sample(self):
        if self.pids is None:
            pids = []
            for path in glob.glob('/proc/*'):
                path = Path(path)
                pid = path.name
                if pid.isdecimal():
                    pids.append(int(pid))
        else:
            pids = self.pids

        self.status = []
        for pid in pids:
            if pid in self.proc and not self.proc[pid].present:
                del self.proc[pid]
                continue

            if pid not in self.proc:
                self.proc[pid] = Proc(pid)

            status = {
                'pid': pid,
                'cmdline': self.proc[pid].cmdline
            }
            self.proc[pid] = Proc(pid)
            status.update(self.proc[pid].sample().asdict())
            self.status.append(status)

        return self.status

    def get_cmdline(self, pid):
        return self.proc[pid].cmdline
