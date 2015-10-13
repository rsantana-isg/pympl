#!/usr/bin/env python
"""
This code is part of the Mathematical Programming Toolbox PyMPL.

Copyright (C) 2015-2015, Filipe Brandao
Faculdade de Ciencias, Universidade do Porto
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

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
"""
from __future__ import print_function
from builtins import map
from builtins import range

import os
import sys
from pympl import PyMPL, glpkutils, script_wsol

if __name__ == "__main__":
    sdir = os.path.dirname(__file__)
    if sdir != "":
        os.chdir(sdir)


def read_tsp(fname):
    """Loads TSP instances."""
    xs, ys = [], []
    with open(fname) as f:
        lst = list(map(float, f.read().split()))
        n = int(lst.pop(0))
        for i in range(n):
            xs.append(lst.pop(0))
            ys.append(lst.pop(0))
    return n, xs, ys


def main():
    """Parses 'tsp.mod'."""

    mod_in = "tsp.mod"
    mod_out = "tmp/tsp.out.mod"
    graph_size = "small"
    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/tsp.lp"
    glpkutils.mod2lp(mod_out, lp_out, True)
    try:
        out, varvalues = script_wsol(
            "vpsolver_gurobi.sh", lp_out, verbose=True
        )
    except Exception as e:
        print(repr(e))

    out, varvalues = script_wsol(
        "glpk_wrapper.sh", lp_out, verbose=True
    )

    print(
        "varvalues:", [
            (k, v)
            for k, v in sorted(varvalues.items()) if not k.startswith("_")
        ]
    )

if __name__ == "__main__":
    main()
