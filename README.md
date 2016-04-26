# SymNet

SymNet is a python program used for symbolic network analysis. It's main
purpose is the extraction of the circuit equations from a electrical
network given as a netlist. SymNet depends on

* sympy or sympycore (for dealing with the symbolic expressions)
* pyparsing (for parsing the netlist)

which are bundled in this repository. Up to now only the basic network
elements are implemented:

* Constant voltage and current sources: V, I
* Passive elements: R, L, C
* Controlled Sources: u = E(u), i = F(i), i = G(u), u = H(i)
* Nullator: U
* Norator: N
* Open circuit: O

Once the network topology of the electric circuit is defined, a tree of this
network must be choosen. A tree is a subgraph of the network which connects
all nodes with some selected branches without making a loop. Afterwards a
node- or loop analysis is used to build up the circuit equations. In case of
the modified nodal analysis (MNA) the standard star-shaped tree is build
automatically.

SymNet is in a very early development stage. The short term tasks are:

* Automatically create the ODE system of a dynamic circuit
* Implement the [Extra Element Therorem](https://en.wikipedia.org/wiki/Extra_element_theorem) (EET)

Any help and especially some application circuits are welcome. Now have fun
with the circuit equations :-)


----

#Example 1: OpAmp

The (non)-inverting OpAmp

```
         +----R1----+
         |          |
         | | \      |
  +--R2--+-|- \     |
  |        |   \ ___| VA
  V2       |   /
  |    +---|+ /
  |    |   | /
  |    V1
  |    |
 ---  ---
```

is modeled with a nullator (U) and a norator (N):

```python
>>> from symnet import *
>>> g, ctrl_src = parse_netlist("""
    V1      pos   GND
    U       pos   neg
    N       out   GND
    R1      neg   out
    R2      neg   1
    V2      1     GND
""")
```

and the circuit equation can be created automatically with the
modified nodal analysis (MNA):

```python
>>> eqs, x, tree = mna(g, ctrl_src, gnd='GND')
>>> A, b = create_matrices(eqs, x)
>>> eqstr = pprint_linear(A, x, b)
>>> print eqstr
```
    [G_R1 + G_R2   -G_R1   0] [Vneg]   =  G_R2*V2
    [      -G_R1    G_R1   1] [Vout]   =  0
    [          1       0   0] [I_N]   =  V1

One should note that in contrast to the standard MNA the equations
for the grounded input voltage sources V1 and V2 are eliminated.

Then sympy can be used to solve this linear system of equations
for Vout:

```python
>>> num, denom = solve_linear(Matrix(A), x, Matrix(b), 'Vout')
>>> pprint(apart(num/denom, Calculus('V1')))
```
      G_R2⋅V₂   V₁⋅(G_R1 + G_R2)
    - ─────── + ────────────────
        G_R1          G_R1

----

# Example 2: Voltage Divider

Here is an example with the simple voltage divider:

```python
>>> from symnet import *
>>> g, ctrl_src = parse_netlist("""
Vin 1 0
R1  1 2
R2  2 0
""")
>>> tree = g.tree(['Vin', 'R2'])
>>> eqs, x = loop_analysis(g, ctrl_src, tree)
>>> A, b = create_matrices(eqs, x)
>>> print pprint_linear(A, x, b)
```
    [R1 + R2] [I_R1]   =  Vin

Then sympy can be used to solve this equation for I_R1:

```python
>>> from sympy import pretty, pprint, simplify, apart
>>> num, denom = solve_linear(Matrix(A), x, Matrix(b), 'I_R1')
>>> pprint(apart(num/denom, Calculus('Vin')))
```
      Vin
    ───────
    R₁ + R₂

By using the modified nodal analysis the tree is build up automatically:

```python
>>> eqs, x, tree = mna(g, ctrl_src)
>>> A, b = create_matrices(eqs, x)
>>> num, denom = solve_linear(Matrix(A), x, Matrix(b), 'V2')
>>> pprint(apart(num/denom, Calculus('Vin')))
```
      G_R1⋅Vin
    ───────────
    G_R1 + G_R2

Further examples can be found in the sources.
