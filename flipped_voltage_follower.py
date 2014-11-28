from symnet import *

"""
Circuit:

    +-----+-------------------------+-----+
   -|     |              OUT        |     |
    Gm1   Rds1                      |     |
   +|     |    X                    |     |
    +-----+-----+-- Rin --+ 1       RS    C2
   +|     |     |        +|         |     |
    Gm2   Rds2  C1        Vin       |     |
   -|     |     |        -|         |     |
    +-----+-----+---------+---------+-----+
          0

Controlled Sources:
    u = E(u)    i = F(i)    i = G(u)    u = H(i)
"""

netlist = """
Vin     1   0
Rin     1   X

C1      X   0
Rds2    X   0
Gm2     X   0   C2

Gm1     X   OUT X 0
Rds1    X   OUT

RS      OUT 0
C2      OUT 0
"""
g, ctrl_src = parse_netlist(netlist)
eqs, x, tree = mna(g, ctrl_src, exclude_grounded_voltage_sources=True)

A, b = create_matrices(eqs, x)
eqstr = pprint_linear(A, x, b)
print eqstr
print

print 'Mathematica:'
print pprint_mathematica(eqs, x)

var = 'VOUT'
num, denom = solve_linear(Matrix(A), x, Matrix(b), var)
num = num.subs('Vin', 1) * Calculus('Vin')  # factor out constant voltage source

num = str(num).replace('G_R', 'G')
denom = str(denom).replace('G_R', 'G')
print
print ' '*8, num
print '%5s ==' %var, '-' * max(len(str(num)), len(str(denom)))
print ' '*8, denom
print

