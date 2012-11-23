import symnet
reload(symnet)
from symnet import *

def test_cut_i_coFi_co():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'R2'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('FM*I_R2*R1 + I_R2*R1 + I_R2*R2 - IQ'),
        Calculus('FM*I_R2*R4 + I_R3*R3 + I_R3*R4 - IQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_coFi_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'R1'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('I_R1*R1 + I_R2*R2 - IQ'),
        Calculus('FM*I_R1*R4 + I_R3*R3 + I_R3*R4 - IQ'),
        Calculus('I_R1 - I_R2 - FM*I_R1')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('I_R1'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_coFi_tr_2():
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
        Calculus('FM*I_IQ*R1 + I_R2*R1 + I_R2*R2 - IQ'),
        Calculus('FM*I_IQ*R4 + I_R3*R3 + I_R3*R4 - IQ'),
        Calculus('I_R2 + I_R3 + I_IQ + FM*I_IQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('I_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_coFi_tr_3():
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
        Calculus('FM*VQ*R1 + I_R2*R1 + I_R2*R2 - V_VQ'),
        Calculus('FM*VQ*R4 + I_R3*R3 + I_R3*R4 - V_VQ'),
        Calculus('VQ + I_R2 + I_R3 + FM*VQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_trFi_tr():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'R1'}

    tree = g.tree(['R1', 'FM', 'R4'])

    vars_ref = [
        Calculus('I_IQ'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_FM'),
    ]
    eqs_ref = [
        Calculus('IQ + I_R2*R4 + I_R3*R1 + I_IQ*R1 + I_IQ*R4 - V_FM'),
        Calculus('I_R2*R2 + I_R2*R4 + I_IQ*R4 - V_FM'),
        Calculus('I_R3*R1 + I_R3*R3 + I_IQ*R1 - V_FM'),
        Calculus('I_R2 + I_R3 + I_IQ - FM*I_R3 - FM*I_IQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_trFi_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'R2'}

    tree = g.tree(['R1', 'FM', 'R4'])

    vars_ref = [
        Calculus('I_IQ'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_FM'),
    ]
    eqs_ref = [
        Calculus('IQ + I_R2*R4 + I_R3*R1 + I_IQ*R1 + I_IQ*R4 - V_FM'),
        Calculus('I_R2*R2 + I_R2*R4 + I_IQ*R4 - V_FM'),
        Calculus('I_R3*R1 + I_R3*R3 + I_IQ*R1 - V_FM'),
        Calculus('I_R2 + I_R3 + I_IQ + FM*I_R2'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref


def test_cut_i_trFi_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('FM', 'L', 'R')
    ctrl_src = {'FM' : 'VQ'}

    tree = g.tree(['R1', 'FM', 'R4'])

    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_FM'),
    ]
    eqs_ref = [
        Calculus('VQ*R4 + I_R2*R2 + I_R2*R4 - V_FM'),
        Calculus('VQ*R1 + I_R3*R1 + I_R3*R3 - V_FM'),
        Calculus('VQ + I_R2 + I_R3 + FM*VQ')
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_coGu_tr_1():
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
        Calculus('GM*R1*V_VQ + I_R2*R1 + I_R2*R2 - V_VQ'),
        Calculus('GM*R4*V_VQ + I_R3*R3 + I_R3*R4 - V_VQ'),
        Calculus('VQ + I_R2 + I_R3 + GM*V_VQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_coGu_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'R1'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('GM*R1*V_R1 + I_R2*R1 + I_R2*R2 - IQ'),
        Calculus('GM*R4*V_R1 + I_R3*R3 + I_R3*R4 - IQ'),
        Calculus('V_R1 - GM*R1*V_R1 - I_R2*R1')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_R1'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_coGu_tr_3():
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
        Calculus('GM*R1*IQ + I_R2*R1 + I_R2*R2 - IQ'),
        Calculus('GM*R4*IQ + I_R3*R3 + I_R3*R4 - IQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_coGu_tr_4():
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
        Calculus('GM*R1*V_VQ + I_R2*R1 + I_R2*R2 - V_VQ'),
        Calculus('GM*R4*V_VQ + I_R3*R3 + I_R3*R4 - V_VQ'),
        Calculus('VQ + I_R2 + I_R3 + GM*V_VQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_coGu_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'VQ'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('GM*R2*V_VQ + GM*R4*V_VQ + VQ*R1 + VQ*R2 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4'),
        Calculus('V_VQ + GM*R2*V_VQ + VQ*R1 + VQ*R2 + I_R3*R1 + I_R3*R2')
    ]
    vars_ref = [
        Calculus('I_R3'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_coGu_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'GM'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('GM*R1*V_GM + I_R2*R1 + I_R2*R2 - IQ'),
        Calculus('GM*R4*V_GM + I_R3*R3 + I_R3*R4 - IQ'),
        Calculus('V_GM + GM*R1*V_GM + GM*R4*V_GM + I_R2*R1 + I_R3*R4 - IQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_GM'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_trGu_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'VQ'}

    tree = g.tree(['R1', 'GM', 'R4'])

    eqs_ref = [
        Calculus('VQ*R4 + I_R2*R2 + I_R2*R4 - V_GM'),
        Calculus('VQ*R1 + I_R3*R1 + I_R3*R3 - V_GM'),
        Calculus('VQ + I_R2 + I_R3 + GM*V_VQ'),
        Calculus('V_VQ + VQ*R1 + VQ*R4 + I_R2*R4 + I_R3*R1 - V_GM')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_GM'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_trGu_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'R2'}

    tree = g.tree(['R1', 'GM', 'R4'])

    eqs_ref = [
        Calculus('VQ*R4 + I_R2*R2 + I_R2*R4 - V_GM'),
        Calculus('VQ*R1 + I_R3*R1 + I_R3*R3 - V_GM'),
        Calculus('VQ + I_R2 + I_R3 + GM*V_R2'),
        Calculus('V_R2 - I_R2*R2')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_GM'),
        Calculus('V_R2'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_trGu_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'GM'}

    tree = g.tree(['R1', 'GM', 'R4'])

    eqs_ref = [
        Calculus('VQ*R4 + I_R2*R2 + I_R2*R4 - V_GM'),
        Calculus('VQ*R1 + I_R3*R1 + I_R3*R3 - V_GM'),
        Calculus('VQ + I_R2 + I_R3 + GM*V_GM')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_GM'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_i_trGu_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('GM', 'L', 'R')
    ctrl_src = {'GM' : 'VQ'}

    tree = g.tree(['VQ', 'GM', 'R4'])

    eqs_ref = [
        Calculus('V_GM + I_R1*R1 + I_R1*R4 + I_R3*R4 - V_VQ - I_R2*R4'),
        Calculus('I_R2*R2 + I_R2*R4 - V_GM - I_R1*R4 - I_R3*R4'),
        Calculus('I_R1*R4 + I_R3*R3 + I_R3*R4 - V_VQ - I_R2*R4'),
        Calculus('VQ + I_R1 + I_R3'),
        Calculus('I_R2 + GM*V_VQ - I_R1')
    ]
    vars_ref = [
        Calculus('I_R1'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_VQ'),
        Calculus('V_GM'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref


#    ****    v = E(v)    ***

def test_cut_v_trEv_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'R1'}

    tree = g.tree(['R1', 'EM', 'R4'])

    eqs_ref = [
        Calculus('VQ*R4 + I_R2*R2 + I_R2*R4 - EM*V_R1'),
        Calculus('VQ*R1 + I_R3*R1 + I_R3*R3 - EM*V_R1'),
        Calculus('V_R1 + VQ*R1 + I_R3*R1')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_R1'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_trEv_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'VQ'}

    tree = g.tree(['VQ', 'EM', 'R4'])

    eqs_ref = [
        Calculus('EM*V_VQ + I_R1*R1 + I_R1*R4 + I_R3*R4 - V_VQ - I_R2*R4'),
        Calculus('I_R2*R2 + I_R2*R4 - EM*V_VQ - I_R1*R4 - I_R3*R4'),
        Calculus('I_R1*R4 + I_R3*R3 + I_R3*R4 - V_VQ - I_R2*R4'),
        Calculus('VQ + I_R1 + I_R3')
    ]
    vars_ref = [
        Calculus('I_R1'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_trEv_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'R2'}

    tree = g.tree(['R1', 'EM', 'R4'])

    eqs_ref = [
        Calculus('VQ*R4 + I_R2*R2 + I_R2*R4 - EM*V_R2'),
        Calculus('VQ*R1 + I_R3*R1 + I_R3*R3 - EM*V_R2'),
        Calculus('V_R2 - I_R2*R2')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_R2'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_trEv_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'VQ'}

    tree = g.tree(['R1', 'EM', 'R4'])

    eqs_ref = [
        Calculus('VQ*R4 + I_R2*R2 + I_R2*R4 - EM*V_VQ'),
        Calculus('VQ*R1 + I_R3*R1 + I_R3*R3 - EM*V_VQ'),
        Calculus('V_VQ + VQ*R1 + VQ*R4 + I_R2*R4 + I_R3*R1 - EM*V_VQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_coEv_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'VQ'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('EM*V_VQ + VQ*R2 + I_EM*R2 + I_EM*R4 + I_R3*R2 + I_R3*R4'),
        Calculus('VQ*R1 + VQ*R2 + I_EM*R2 + I_EM*R4 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4'),
        Calculus('V_VQ + VQ*R1 + VQ*R2 + I_EM*R2 + I_R3*R1 + I_R3*R2')
    ]
    vars_ref = [
        Calculus('I_EM'),
        Calculus('I_R3'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_coEv_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'R3'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('EM*V_R3 + VQ*R2 + I_EM*R2 + I_EM*R4 + I_R3*R2 + I_R3*R4'),
        Calculus('VQ*R1 + VQ*R2 + I_EM*R2 + I_EM*R4 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4'),
        Calculus('V_R3 - I_R3*R3')
    ]
    vars_ref = [
        Calculus('I_EM'),
        Calculus('I_R3'),
        Calculus('V_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_coEv_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'IQ'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('EM*IQ + I_EM*R1 + I_EM*R4 + I_R2*R1 + I_R3*R4 - IQ'),
        Calculus('I_EM*R1 + I_R2*R1 + I_R2*R2 - IQ'),
        Calculus('I_EM*R4 + I_R3*R3 + I_R3*R4 - IQ')
    ]
    vars_ref = [
        Calculus('I_EM'),
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_coEv_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('EM', 'L', 'R')
    ctrl_src = {'EM' : 'R1'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('EM*V_R1 + I_EM*R1 + I_EM*R4 + I_R2*R1 + I_R3*R4 - IQ'),
        Calculus('I_EM*R1 + I_R2*R1 + I_R2*R2 - IQ'),
        Calculus('I_EM*R4 + I_R3*R3 + I_R3*R4 - IQ'),
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

def test_cut_v_trHi_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'HM'}

    tree = g.tree(['R1', 'HM', 'R4'])

    eqs_ref = [
        Calculus('HM*VQ + HM*I_R2 + HM*I_R3 + VQ*R4 + I_R2*R2 + I_R2*R4'),
        Calculus('HM*VQ + HM*I_R2 + HM*I_R3 + VQ*R1 + I_R3*R1 + I_R3*R3')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_trHi_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'VQ'}

    tree = g.tree(['VQ', 'HM', 'R4'])

    eqs_ref = [
        Calculus('HM*VQ + I_R1*R1 + I_R1*R4 + I_R3*R4 - V_VQ - I_R2*R4'),
        Calculus('I_R2*R2 + I_R2*R4 - HM*VQ - I_R1*R4 - I_R3*R4'),
        Calculus('I_R1*R4 + I_R3*R3 + I_R3*R4 - V_VQ - I_R2*R4'),
        Calculus('VQ + I_R1 + I_R3')
    ]
    vars_ref = [
        Calculus('I_R1'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_trHi_tr_3():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'HM'}

    tree = g.tree(['VQ', 'HM', 'R4'])

    eqs_ref = [
        Calculus('HM*VQ + I_R1*R1 + I_R1*R4 + I_R3*R4 - V_VQ - I_R2*R4'),
        Calculus('I_R2*R2 + I_R2*R4 - HM*VQ - I_R1*R4 - I_R3*R4'),
        Calculus('I_R1*R4 + I_R3*R3 + I_R3*R4 - V_VQ - I_R2*R4'),
        Calculus('VQ + I_R1 + I_R3')
    ]
    vars_ref = [
        Calculus('I_R1'),
        Calculus('I_R2'),
        Calculus('I_R3'),
        Calculus('V_VQ'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_trHi_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'R2'}

    tree = g.tree(['R1', 'HM', 'R4'])

    eqs_ref = [
        Calculus('VQ*R4 + I_R2*R2 + I_R2*R4 - HM*I_R2'),
        Calculus('VQ*R1 + I_R3*R1 + I_R3*R3 - HM*I_R2')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_trHi_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'VQ'}

    tree = g.tree(['R1', 'HM', 'R4'])

    eqs_ref = [
        Calculus('VQ*R4 + I_R2*R2 + I_R2*R4 - HM*VQ'),
        Calculus('VQ*R1 + I_R3*R1 + I_R3*R3 - HM*VQ')
    ]
    vars_ref = [
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_coHi_co_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'VQ'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('HM*VQ + VQ*R2 + I_HM*R2 + I_HM*R4 + I_R3*R2 + I_R3*R4'),
        Calculus('VQ*R1 + VQ*R2 + I_HM*R2 + I_HM*R4 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4')
    ]
    vars_ref = [
        Calculus('I_HM'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_coHi_co_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('VQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'R3'}

    tree = g.tree(['R1', 'R2', 'R4'])

    eqs_ref = [
        Calculus('HM*I_R3 + VQ*R2 + I_HM*R2 + I_HM*R4 + I_R3*R2 + I_R3*R4'),
        Calculus('VQ*R1 + VQ*R2 + I_HM*R2 + I_HM*R4 + I_R3*R1 + I_R3*R2 + I_R3*R3 + I_R3*R4')
    ]
    vars_ref = [
        Calculus('I_HM'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_coHi_tr_1():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'IQ'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('I_HM*R1 + I_HM*R4 + I_R2*R1 + I_R3*R4 - IQ - HM*I_HM - HM*I_R2 - HM*I_R3'),
        Calculus('I_HM*R1 + I_R2*R1 + I_R2*R2 - IQ'),
        Calculus('I_HM*R4 + I_R3*R3 + I_R3*R4 - IQ')
    ]
    vars_ref = [
        Calculus('I_HM'),
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

def test_cut_v_coHi_tr_2():
    g = Graph()
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('IQ', 'A', '0')
    g.add_branch('HM', 'L', 'R')
    ctrl_src = {'HM' : 'R1'}

    tree = g.tree(['R1', 'IQ', 'R4'])

    eqs_ref = [
        Calculus('HM*I_HM + HM*I_R2 + I_HM*R1 + I_HM*R4 + I_R2*R1 + I_R3*R4 - IQ'),
        Calculus('I_HM*R1 + I_R2*R1 + I_R2*R2 - IQ'),
        Calculus('I_HM*R4 + I_R3*R3 + I_R3*R4 - IQ')
    ]
    vars_ref = [
        Calculus('I_HM'),
        Calculus('I_R2'),
        Calculus('I_R3'),
    ]
    return g, ctrl_src, tree, eqs_ref, vars_ref

tests = [
    test_cut_i_coFi_co,
    test_cut_i_coFi_tr_1,
    test_cut_i_coFi_tr_2,
    test_cut_i_coFi_tr_3,
    test_cut_i_trFi_tr,
    test_cut_i_trFi_co_1,
    test_cut_i_trFi_co_2,

    test_cut_i_coGu_tr_1,
    test_cut_i_coGu_tr_2,
    test_cut_i_coGu_tr_3,
    test_cut_i_coGu_tr_4,
    test_cut_i_coGu_co_1,
    test_cut_i_coGu_co_2,
    test_cut_i_trGu_co_1,
    test_cut_i_trGu_co_2,
    test_cut_i_trGu_tr_1,
    test_cut_i_trGu_tr_2,

    test_cut_v_trEv_tr_1,
    test_cut_v_trEv_tr_2,
    test_cut_v_trEv_co_1,
    test_cut_v_trEv_co_2,  # no substitutable equ for v_ctrl
    test_cut_v_coEv_co_1,
    test_cut_v_coEv_co_2,
    test_cut_v_coEv_tr_1,
    test_cut_v_coEv_tr_2,

    # Ab hier iO
    test_cut_v_trHi_tr_1,  # acts like a resistor
    test_cut_v_trHi_tr_2,
    test_cut_v_trHi_tr_3,  # like resistor with same tree as test before

    test_cut_v_trHi_co_1,
    test_cut_v_trHi_co_2,
    test_cut_v_coHi_co_1,
    test_cut_v_coHi_co_2,
    test_cut_v_coHi_tr_1,
    test_cut_v_coHi_tr_2,
]

if __name__ == '__main__2':
    from sympycore import Matrix

    print '\n    **** Test Schnittanalyse ****\n'
    for test_func in tests:
        print '*', test_func.__name__
        g, ctrl_src, tree, eqs_ref, vars_ref = test_func()
        treebrns = tree.branches()
        cobrns = g.branches() - treebrns
        #~ print '  Baum', treebrns, ',  Ctrls', ctrl_src, ',  Cobaum', cobrns
        eqs, vars = cut_analysis(g, ctrl_src, tree)
        #~ if not eqs_ref == eqs: print '*** !!! Equations different !!! ***'
        #~ if not vars_ref == vars: print '*** !!! Variables different !!! ***'

if __name__ == '__main__':
    from sympycore import Matrix

    print '\n    **** Test Schnittanalyse ****\n'
    for test_func in tests:
        print '*', test_func.__name__
        g, ctrl_src, tree, eqs_ref, vars_ref = test_func()
        treebrns = tree.branches()
        cobrns = g.branches() - treebrns
        print '  Baum', treebrns, ',  Ctrls', ctrl_src, ',  Cobaum', cobrns
        eqs, vars = cut_analysis(g, ctrl_src, tree)
        #~ if not eqs_ref == eqs: print '*** !!! Equations different !!! ***'
        #~ if not vars_ref == vars: print '*** !!! Variables different !!! ***'
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
