# This file is part of Marcel.
# 
# Marcel is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or at your
# option) any later version.
# 
# Marcel is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Marcel.  If not, see <https://www.gnu.org/licenses/>.

import marcel.argsparser
import marcel.core


HELP = '''
{L,wrap=F}head N

{L,indent=4:28}{r:N}                       The number of input tuples to be written to output.

Output the first {r:N} tuples of the input stream, and discard the others.  
'''


def head(env, n):
    return Head(env), [n]


class HeadArgsParser(marcel.argsparser.ArgsParser):

    def __init__(self, env):
        super().__init__('head', env)
        self.add_anon('n', convert=self.str_to_int, target='n_arg')
        self.validate()


class Head(marcel.core.Op):

    def __init__(self, env):
        super().__init__(env)
        self.n_arg = None
        self.n = None
        self.received = None

    def __repr__(self):
        return f'head({self.n})'

    # AbstractOp
    
    def setup(self):
        self.n = self.eval_function('n_arg', int)
        self.received = 0

    def receive(self, x):
        self.received += 1
        if self.n >= self.received:
            self.send(x)
