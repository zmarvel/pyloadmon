
# pyloadmon

Library for monitoring Linux process status.

## Example

This depends on the `tabulate` module. It will print a process table, sorted by
PID.

```python
from pyloadmon import Sampler
from tabulate import tabulate

sampler = Sampler()
status = sampler.sample()
status = status.sort(key=lambda st: st['pid'])
print(tabulate(status, headers='keys'))
```

## License

This project is distributed under the GPLv3.0.

Copyright (C) 2020  Zack Marvel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

