import symnet
reload(symnet)
from symnet import *

def test_loop_i_coFi_co():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'R2'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('FM*I_R2*R1 + I_R2*R1 + I_R2*R2 - VQ'),
        Calculus('FM*I_R2*R4 + I_R3*R3 + I_R3*R4 - VQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_coFi_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'R1'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('I_R1*R1 + I_R2*R2 - VQ'),
        Calculus('FM*I_R1*R4 + I_R3*R3 + I_R3*R4 - VQ'),
        Calculus('I_R1 - I_R2 - FM*I_R1')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('I_R1'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_coFi_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'VQ'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('FM*I_VQ*R1 + I_R2*R1 + I_R2*R2 - VQ'),
        Calculus('FM*I_VQ*R4 + I_R3*R3 + I_R3*R4 - VQ'),
        Calculus('I_R2 + I_R3 + I_VQ + FM*I_VQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('I_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_coFi_tr_3():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'IQ'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('FM*IQ*R1 + I_R2*R1 + I_R2*R2 - V_IQ'),
        Calculus('FM*IQ*R4 + I_R3*R3 + I_R3*R4 - V_IQ'),
        Calculus('IQ + I_R2 + I_R3 + FM*IQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_trFi_tr():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'R1'}

    tree = g.tree(['R1', 'FM', 'R4'])

    vars_ref = [
        Calculus('I_VQ'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_FM'),
    ]
    eqs_ref = [
        Calculus('VQ + I_R2*R4 + I_R3*R1 + I_VQ*R1 + I_VQ*R4 - V_FM'),
        Calculus('I_R2*R2 + I_R2*R4 + I_VQ*R4 - V_FM'),
        Calculus('I_R3*R1 + I_R3*R3 + I_VQ*R1 - V_FM'),
        Calculus('I_R2 + I_R3 + I_VQ - FM*I_R3 - FM*I_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_trFi_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'R2'}

    tree = g.tree(['R1', 'FM', 'R4'])

    vars_ref = [
        Calculus('I_VQ'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_FM'),
    ]
    eqs_ref = [
        Calculus('VQ + I_R2*R4 + I_R3*R1 + I_VQ*R1 + I_VQ*R4 - V_FM'),
        Calculus('I_R2*R2 + I_R2*R4 + I_VQ*R4 - V_FM'),
        Calculus('I_R3*R1 + I_R3*R3 + I_VQ*R1 - V_FM'),
        Calculus('I_R2 + I_R3 + I_VQ + FM*I_R2'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref


def test_loop_i_trFi_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'IQ'}

    tree = g.tree(['R1', 'FM', 'R4'])

    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_FM'),
    ]
    eqs_ref = [
        Calculus('IQ*R4 + I_R2*R2 + I_R2*R4 - V_FM'),
        Calculus('IQ*R1 + I_R3*R1 + I_R3*R3 - V_FM'),
        Calculus('IQ + I_R2 + I_R3 + FM*IQ')
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_coGu_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'IQ'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('GM*R1*V_IQ + I_R2*R1 + I_R2*R2 - V_IQ'),
        Calculus('GM*R4*V_IQ + I_R3*R3 + I_R3*R4 - V_IQ'),
        Calculus('IQ + I_R2 + I_R3 + GM*V_IQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_coGu_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'R1'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('GM*R1*V_R1 + I_R2*R1 + I_R2*R2 - VQ'),
        Calculus('GM*R4*V_R1 + I_R3*R3 + I_R3*R4 - VQ'),
        Calculus('V_R1 - GM*R1*V_R1 - I_R2*R1')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_R1'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_coGu_tr_3():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'VQ'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('GM*R1*VQ + I_R2*R1 + I_R2*R2 - VQ'),
        Calculus('GM*R4*VQ + I_R3*R3 + I_R3*R4 - VQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_coGu_tr_4():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'IQ'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('GM*R1*V_IQ + I_R2*R1 + I_R2*R2 - V_IQ'),
        Calculus('GM*R4*V_IQ + I_R3*R3 + I_R3*R4 - V_IQ'),
        Calculus('IQ + I_R2 + I_R3 + GM*V_IQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_coGu_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'IQ'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('GM*R2*V_IQ + GM*R4*V_IQ + IQ*R1 + IQ*R2 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4'),
        Calculus('V_IQ + GM*R2*V_IQ + IQ*R1 + IQ*R2 + I_R3*R1 + I_R3*R2')
    ]
    vars_ref = [
        Calculus('I_R3'),
        Calculus('V_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_coGu_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'GM'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('GM*R1*V_GM + I_R2*R1 + I_R2*R2 - VQ'),
        Calculus('GM*R4*V_GM + I_R3*R3 + I_R3*R4 - VQ'),
        Calculus('V_GM + GM*R1*V_GM + GM*R4*V_GM + I_R2*R1 + I_R3*R4 - VQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_GM'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_trGu_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'IQ'}

    tree = g.tree(['R1', 'GM', 'R4'])

    eqs_ref = [
        Calculus('IQ*R4 + I_R2*R2 + I_R2*R4 - V_GM'),
        Calculus('IQ*R1 + I_R3*R1 + I_R3*R3 - V_GM'),
        Calculus('IQ + I_R2 + I_R3 + GM*V_IQ'),
        Calculus('V_IQ + IQ*R1 + IQ*R4 + I_R2*R4 + I_R3*R1 - V_GM')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_GM'),
        Calculus('V_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_trGu_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'R2'}

    tree = g.tree(['R1', 'GM', 'R4'])

    eqs_ref = [
        Calculus('IQ*R4 + I_R2*R2 + I_R2*R4 - V_GM'),
        Calculus('IQ*R1 + I_R3*R1 + I_R3*R3 - V_GM'),
        Calculus('IQ + I_R2 + I_R3 + GM*V_R2'),
        Calculus('V_R2 - I_R2*R2')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_GM'),
        Calculus('V_R2'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_trGu_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'GM'}

    tree = g.tree(['R1', 'GM', 'R4'])

    eqs_ref = [
        Calculus('IQ*R4 + I_R2*R2 + I_R2*R4 - V_GM'),
        Calculus('IQ*R1 + I_R3*R1 + I_R3*R3 - V_GM'),
        Calculus('IQ + I_R2 + I_R3 + GM*V_GM')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_GM'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_i_trGu_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'IQ'}

    tree = g.tree(['IQ', 'GM', 'R4'])

    eqs_ref = [
        Calculus('V_GM + I_R1*R1 + I_R1*R4 + I_R3*R4 - V_IQ - I_R2*R4'),
        Calculus('I_R2*R2 + I_R2*R4 - V_GM - I_R1*R4 - I_R3*R4'),
        Calculus('I_R1*R4 + I_R3*R3 + I_R3*R4 - V_IQ - I_R2*R4'),
        Calculus('IQ + I_R1 + I_R3'),
        Calculus('I_R2 + GM*V_IQ - I_R1')
    ]
    vars_ref = [
        Calculus('I_R1'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_IQ'),
        Calculus('V_GM'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref


#    ****    v = E(v)    ***

def test_loop_v_trEv_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'R1'}

    tree = g.tree(['R1', 'EM', 'R4'])

    eqs_ref = [
        Calculus('IQ*R4 + I_R2*R2 + I_R2*R4 - EM*V_R1'),
        Calculus('IQ*R1 + I_R3*R1 + I_R3*R3 - EM*V_R1'),
        Calculus('V_R1 + IQ*R1 + I_R3*R1')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_R1'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_trEv_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'IQ'}

    tree = g.tree(['IQ', 'EM', 'R4'])

    eqs_ref = [
        Calculus('EM*V_IQ + I_R1*R1 + I_R1*R4 + I_R3*R4 - V_IQ - I_R2*R4'),
        Calculus('I_R2*R2 + I_R2*R4 - EM*V_IQ - I_R1*R4 - I_R3*R4'),
        Calculus('I_R1*R4 + I_R3*R3 + I_R3*R4 - V_IQ - I_R2*R4'),
        Calculus('IQ + I_R1 + I_R3')
    ]
    vars_ref = [
        Calculus('I_R1'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_trEv_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'R2'}

    tree = g.tree(['R1', 'EM', 'R4'])

    eqs_ref = [
        Calculus('IQ*R4 + I_R2*R2 + I_R2*R4 - EM*V_R2'),
        Calculus('IQ*R1 + I_R3*R1 + I_R3*R3 - EM*V_R2'),
        Calculus('V_R2 - I_R2*R2')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_R2'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_trEv_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'IQ'}

    tree = g.tree(['R1', 'EM', 'R4'])

    eqs_ref = [
        Calculus('IQ*R4 + I_R2*R2 + I_R2*R4 - EM*V_IQ'),
        Calculus('IQ*R1 + I_R3*R1 + I_R3*R3 - EM*V_IQ'),
        Calculus('V_IQ + IQ*R1 + IQ*R4 + I_R2*R4 + I_R3*R1 - EM*V_IQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_coEv_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'IQ'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('EM*V_IQ + IQ*R2 + I_EM*R2 + I_EM*R4 + I_R3*R2 + I_R3*R4'),
        Calculus('IQ*R1 + IQ*R2 + I_EM*R2 + I_EM*R4 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4'),
        Calculus('V_IQ + IQ*R1 + IQ*R2 + I_EM*R2 + I_R3*R1 + I_R3*R2')
    ]
    vars_ref = [
        Calculus('I_EM'),
        Calculus('I_R3'),
        Calculus('V_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_coEv_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'R3'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('EM*V_R3 + IQ*R2 + I_EM*R2 + I_EM*R4 + I_R3*R2 + I_R3*R4'),
        Calculus('IQ*R1 + IQ*R2 + I_EM*R2 + I_EM*R4 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4'),
        Calculus('V_R3 - I_R3*R3')
    ]
    vars_ref = [
        Calculus('I_EM'),
        Calculus('I_R3'),
        Calculus('V_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_coEv_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'VQ'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('EM*VQ + I_EM*R1 + I_EM*R4 + I_R2*R1 + I_R3*R4 - VQ'),
        Calculus('I_EM*R1 + I_R2*R1 + I_R2*R2 - VQ'),
        Calculus('I_EM*R4 + I_R3*R3 + I_R3*R4 - VQ')
    ]
    vars_ref = [
        Calculus('I_EM'),
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_coEv_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'R1'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('EM*V_R1 + I_EM*R1 + I_EM*R4 + I_R2*R1 + I_R3*R4 - VQ'),
        Calculus('I_EM*R1 + I_R2*R1 + I_R2*R2 - VQ'),
        Calculus('I_EM*R4 + I_R3*R3 + I_R3*R4 - VQ'),
        Calculus('V_R1 - I_EM*R1 - I_R2*R1')
    ]
    vars_ref = [
        Calculus('I_EM'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_R1'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref


#    ****    v = H(i)    ***

def test_loop_v_trHi_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'HM'}

    tree = g.tree(['R1', 'HM', 'R4'])

    eqs_ref = [
        Calculus('HM*IQ + HM*I_R2 + HM*I_R3 + IQ*R4 + I_R2*R2 + I_R2*R4'),
        Calculus('HM*IQ + HM*I_R2 + HM*I_R3 + IQ*R1 + I_R3*R1 + I_R3*R3')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_trHi_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'IQ'}

    tree = g.tree(['IQ', 'HM', 'R4'])

    eqs_ref = [
        Calculus('HM*IQ + I_R1*R1 + I_R1*R4 + I_R3*R4 - V_IQ - I_R2*R4'),
        Calculus('I_R2*R2 + I_R2*R4 - HM*IQ - I_R1*R4 - I_R3*R4'),
        Calculus('I_R1*R4 + I_R3*R3 + I_R3*R4 - V_IQ - I_R2*R4'),
        Calculus('IQ + I_R1 + I_R3')
    ]
    vars_ref = [
        Calculus('I_R1'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_trHi_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'R2'}

    tree = g.tree(['R1', 'HM', 'R4'])

    eqs_ref = [
        Calculus('IQ*R4 + I_R2*R2 + I_R2*R4 - HM*I_R2'),
        Calculus('IQ*R1 + I_R3*R1 + I_R3*R3 - HM*I_R2')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_trHi_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'IQ'}

    tree = g.tree(['R1', 'HM', 'R4'])

    eqs_ref = [
        Calculus('IQ*R4 + I_R2*R2 + I_R2*R4 - HM*IQ'),
        Calculus('IQ*R1 + I_R3*R1 + I_R3*R3 - HM*IQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_coHi_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'IQ'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('HM*IQ + IQ*R2 + I_HM*R2 + I_HM*R4 + I_R3*R2 + I_R3*R4'),
        Calculus('IQ*R1 + IQ*R2 + I_HM*R2 + I_HM*R4 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4')
    ]
    vars_ref = [
        Calculus('I_HM'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_coHi_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'R3'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('HM*I_R3 + IQ*R2 + I_HM*R2 + I_HM*R4 + I_R3*R2 + I_R3*R4'),
        Calculus('IQ*R1 + IQ*R2 + I_HM*R2 + I_HM*R4 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4')
    ]
    vars_ref = [
        Calculus('I_HM'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_coHi_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'VQ'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('I_HM*R1 + I_HM*R4 + I_R2*R1 + I_R3*R4 - VQ - HM*I_HM - HM*I_R2 - HM*I_R3'),
        Calculus('I_HM*R1 + I_R2*R1 + I_R2*R2 - VQ'),
        Calculus('I_HM*R4 + I_R3*R3 + I_R3*R4 - VQ')
    ]
    vars_ref = [
        Calculus('I_HM'),
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_loop_v_coHi_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'R1'}

    tree = g.tree(['R1', 'VQ', 'R4'])

    eqs_ref = [
        Calculus('HM*I_HM + HM*I_R2 + I_HM*R1 + I_HM*R4 + I_R2*R1 + I_R3*R4 - VQ'),
        Calculus('I_HM*R1 + I_R2*R1 + I_R2*R2 - VQ'),
        Calculus('I_HM*R4 + I_R3*R3 + I_R3*R4 - VQ')
    ]
    vars_ref = [
        Calculus('I_HM'),
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

tests = [
    test_loop_i_coFi_co,
    test_loop_i_coFi_tr_1,
    test_loop_i_coFi_tr_2,
    test_loop_i_coFi_tr_3,
    test_loop_i_trFi_tr,
    test_loop_i_trFi_co_1,
    test_loop_i_trFi_co_2,

    test_loop_i_coGu_tr_1,
    test_loop_i_coGu_tr_2,
    test_loop_i_coGu_tr_3,
    test_loop_i_coGu_tr_4,
    test_loop_i_coGu_co_1,
    test_loop_i_coGu_co_2,
    test_loop_i_trGu_co_1,
    test_loop_i_trGu_co_2,
    test_loop_i_trGu_tr_1,
    test_loop_i_trGu_tr_2,

    test_loop_v_trEv_tr_1,
    test_loop_v_trEv_tr_2,
    test_loop_v_trEv_co_1,
    test_loop_v_trEv_co_2,  # no substitutable equ for v_ctrl
    test_loop_v_coEv_co_1,
    test_loop_v_coEv_co_2,
    test_loop_v_coEv_tr_1,
    test_loop_v_coEv_tr_2,

    test_loop_v_trHi_tr_1,  # acts like a resistor
    test_loop_v_trHi_tr_2,
    test_loop_v_trHi_co_1,
    test_loop_v_trHi_co_2,
    test_loop_v_coHi_co_1,
    test_loop_v_coHi_co_2,
    test_loop_v_coHi_tr_1,
    test_loop_v_coHi_tr_2,
]

if __name__ == '__main__':
    from sympycore import Matrix

    print '\n    **** Test Maschenanalyse ****\n'
    for test_func in tests:
        print '*', test_func.__name__
        g, ctrl_src, tree, eqs_ref, vars_ref = test_func()
        treebrns = tree.branches()
        cobrns = g.branches() - treebrns
        #~ print '  Baum', treebrns, ',  Ctrls', ctrl_src, ',  Cobaum', cobrns
        eqs, vars = loop_analysis(g, ctrl_src, tree)
        if not eqs_ref == eqs: print '*** !!! Equations different !!! ***'
        if not vars_ref == vars: print '*** !!! Variables different !!! ***'

if False:
    from sympycore import Matrix

    print '\n    **** Test Maschenanalyse ****\n'
    for test_func in tests:
        print '*', test_func.__name__
        g, ctrl_src, tree, eqs_ref, vars_ref = test_func()
        treebrns = tree.branches()
        cobrns = g.branches() - treebrns
        print '  Baum', treebrns, ',  Ctrls', ctrl_src, ',  Cobaum', cobrns
        eqs, vars = loop_analysis(g, ctrl_src, tree)
        if not eqs_ref == eqs: print '*** !!! Equations different !!! ***'
        if not vars_ref == vars: print '*** !!! Variables different !!! ***'
        A, b = create_matrices(eqs, vars)
        # pretty print of the matrix equation
        eqs_str = [str(Matrix(M)).split('\n') for M in A, vars, b]
        for e, v, r in zip(*eqs_str):
            print '[%s] [%s]   =  %s' % (e, v, r)
        if len(eqs) > len(vars):
            print '\n!!! Zuwenig Unbekannte !!!'
        if len(eqs) < len(vars):
            print '\n!!! Zuwenig Gleichungen !!!'
        print
