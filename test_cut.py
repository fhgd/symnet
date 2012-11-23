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

    result = """
[ G_R3 + G_R4            0        -G_R3  -FM] [ V_R4]   =     0
[           0  G_R1 + G_R2        -G_R2  -FM] [ V_R1]   =     0
[       -G_R3        -G_R2  G_R2 + G_R3   FM] [ V_IQ]   =   -IQ
[           0         G_R2        -G_R2    1] [ I_R2]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4            0        -G_R3  -FM] [ V_R4]   =     0
[           0  G_R1 + G_R2        -G_R2  -FM] [ V_R1]   =     0
[       -G_R3        -G_R2  G_R2 + G_R3   FM] [ V_IQ]   =   -IQ
[           0        -G_R1            0    1] [ I_R1]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4            0        -G_R3] [ V_R4]   =         FM*IQ
[           0  G_R1 + G_R2        -G_R2] [ V_R1]   =         FM*IQ
[       -G_R3        -G_R2  G_R2 + G_R3] [ V_IQ]   =   -IQ - FM*IQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4            0     -FM] [ V_R4]   =              G_R3*VQ
[           0  G_R1 + G_R2     -FM] [ V_R1]   =              G_R2*VQ
[       -G_R3        -G_R2  1 + FM] [ I_VQ]   =   -G_R2*VQ - G_R3*VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R2 + G_R4            0         G_R2   0] [ V_R4]   =   -IQ
[           0  G_R1 + G_R3         G_R3   0] [ V_R1]   =   -IQ
[        G_R2         G_R3  G_R2 + G_R3  FM] [ V_FM]   =   -IQ
[           0        -G_R1            0   1] [ I_R1]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R2 + G_R4            0         G_R2   0] [ V_R4]   =   -IQ
[           0  G_R1 + G_R3         G_R3   0] [ V_R1]   =   -IQ
[        G_R2         G_R3  G_R2 + G_R3  FM] [ V_FM]   =   -IQ
[       -G_R2            0        -G_R2   1] [ I_R2]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R2 + G_R4            0         G_R2       1] [ V_R4]   =     0
[           0  G_R1 + G_R3         G_R3       1] [ V_R1]   =     0
[        G_R2         G_R3  G_R2 + G_R3  1 + FM] [ V_FM]   =     0
[          -1           -1           -1       0] [ I_VQ]   =   -VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4            0] [ V_R4]   =   GM*VQ + G_R3*VQ
[           0  G_R1 + G_R2] [ V_R1]   =   GM*VQ + G_R2*VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4               -GM        -G_R3] [ V_R4]   =     0
[           0  G_R1 + G_R2 - GM        -G_R2] [ V_R1]   =     0
[       -G_R3         GM - G_R2  G_R2 + G_R3] [ V_IQ]   =   -IQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4            0        -GM - G_R3] [ V_R4]   =     0
[           0  G_R1 + G_R2        -GM - G_R2] [ V_R1]   =     0
[       -G_R3        -G_R2  GM + G_R2 + G_R3] [ V_IQ]   =   -IQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4            0] [ V_R4]   =   GM*VQ + G_R3*VQ
[           0  G_R1 + G_R2] [ V_R1]   =   GM*VQ + G_R2*VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4        -G_R3        -G_R3  0] [ V_R4]   =    GM*VQ
[       -G_R3  G_R1 + G_R3         G_R3  1] [ V_R1]   =        0
[       -G_R3         G_R3  G_R2 + G_R3  1] [ V_R2]   =   -GM*VQ
[           0           -1           -1  0] [ I_VQ]   =      -VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ GM + G_R3 + G_R4                GM        -GM - G_R3] [ V_R4]   =     0
[               GM  GM + G_R1 + G_R2        -GM - G_R2] [ V_R1]   =     0
[       -GM - G_R3        -GM - G_R2  GM + G_R2 + G_R3] [ V_IQ]   =   -IQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R2 + G_R4            0         G_R2  1] [ V_R4]   =        0
[           0  G_R1 + G_R3         G_R3  1] [ V_R1]   =        0
[        G_R2         G_R3  G_R2 + G_R3  1] [ V_GM]   =   -GM*VQ
[          -1           -1           -1  0] [ I_VQ]   =      -VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R2 + G_R4            0              G_R2  1] [ V_R4]   =     0
[           0  G_R1 + G_R3              G_R3  1] [ V_R1]   =     0
[   GM + G_R2         G_R3  GM + G_R2 + G_R3  1] [ V_GM]   =     0
[          -1           -1                -1  0] [ I_VQ]   =   -VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R2 + G_R4            0              G_R2  1] [ V_R4]   =     0
[           0  G_R1 + G_R3              G_R3  1] [ V_R1]   =     0
[        G_R2         G_R3  GM + G_R2 + G_R3  1] [ V_GM]   =     0
[          -1           -1                -1  0] [ I_VQ]   =   -VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R1 + G_R2 + G_R3 + G_R4  G_R1 + G_R2] [ V_R4]   =   G_R1*VQ + G_R3*VQ
[               G_R1 + G_R2  G_R1 + G_R2] [ V_GM]   =     G_R1*VQ - GM*VQ
    """
    return g, ctrl_src, tree, result


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
    result = """
[ G_R2 + G_R4                EM*G_R2  1] [ V_R4]   =     0
[           0  G_R1 + G_R3 + EM*G_R3  1] [ V_R1]   =     0
[          -1                -1 - EM  0] [ I_VQ]   =   -VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R1 + G_R2 + G_R3 + G_R4] [ V_R4]   =   G_R1*VQ + G_R3*VQ - EM*G_R1*VQ - EM*G_R2*VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R4            0  1     G_R2] [ V_R4]   =     0
[    0  G_R1 + G_R3  1  EM*G_R3] [ V_R1]   =     0
[   -1           -1  0      -EM] [ I_VQ]   =   -VQ
[   -1            0  0   1 - EM] [ V_R2]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R2 + G_R4            0  1] [ V_R4]   =   -EM*G_R2*VQ
[           0  G_R1 + G_R3  1] [ V_R1]   =   -EM*G_R3*VQ
[          -1           -1  0] [ I_VQ]   =    EM*VQ - VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4        -G_R3        -G_R3  -1  0] [ V_R4]   =        0
[       -G_R3  G_R1 + G_R3         G_R3   0  1] [ V_R1]   =        0
[       -G_R3         G_R3  G_R2 + G_R3   1  1] [ V_R2]   =        0
[           1            0           -1   0  0] [ I_EM]   =   -EM*VQ
[           0           -1           -1   0  0] [ I_VQ]   =      -VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4        -G_R3        -G_R3  -1  0] [ V_R4]   =     0
[       -G_R3  G_R1 + G_R3         G_R3   0  1] [ V_R1]   =     0
[       -G_R3         G_R3  G_R2 + G_R3   1  1] [ V_R2]   =     0
[      1 - EM           EM       EM - 1   0  0] [ I_EM]   =     0
[           0           -1           -1   0  0] [ I_VQ]   =   -VQ
    """
    return g, ctrl_src, tree, result

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
    result = """
[ G_R3 + G_R4            0        -G_R3  -1] [ V_R4]   =     0
[           0  G_R1 + G_R2        -G_R2  -1] [ V_R1]   =     0
[       -G_R3        -G_R2  G_R2 + G_R3   1] [ V_IQ]   =   -IQ
[           1            1       EM - 1   0] [ I_EM]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4            0        -G_R3  -1] [ V_R4]   =     0
[           0  G_R1 + G_R2        -G_R2  -1] [ V_R1]   =     0
[       -G_R3        -G_R2  G_R2 + G_R3   1] [ V_IQ]   =   -IQ
[           1       1 + EM           -1   0] [ I_EM]   =     0
    """
    return g, ctrl_src, tree, result


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

    result = """
[ G_R2 + G_R4            0  1                G_R2*HM] [ V_R4]   =     0
[           0  G_R1 + G_R3  1                G_R3*HM] [ V_R1]   =     0
[          -1           -1  0                    -HM] [ I_VQ]   =   -VQ
[        G_R2         G_R3  1  1 + G_R2*HM + G_R3*HM] [ I_HM]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R1 + G_R2 + G_R3 + G_R4  G_R1*HM + G_R2*HM] [ V_R4]   =    G_R1*VQ + G_R3*VQ
[              -G_R1 - G_R3        1 - G_R1*HM] [ I_VQ]   =   -G_R1*VQ - G_R3*VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R1 + G_R2 + G_R3 + G_R4      G_R1*HM + G_R2*HM] [ V_R4]   =   G_R1*VQ + G_R3*VQ
[               G_R1 + G_R2  1 + G_R1*HM + G_R2*HM] [ I_HM]   =             G_R1*VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R2 + G_R4            0  1      G_R2*HM] [ V_R4]   =     0
[           0  G_R1 + G_R3  1      G_R3*HM] [ V_R1]   =     0
[          -1           -1  0          -HM] [ I_VQ]   =   -VQ
[       -G_R2            0  0  1 - G_R2*HM] [ I_R2]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R2 + G_R4            0  1 + G_R2*HM] [ V_R4]   =     0
[           0  G_R1 + G_R3  1 + G_R3*HM] [ V_R1]   =     0
[          -1           -1          -HM] [ I_VQ]   =   -VQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4        -G_R3        -G_R3   0  -1] [ V_R4]   =     0
[       -G_R3  G_R1 + G_R3         G_R3   1   0] [ V_R1]   =     0
[       -G_R3         G_R3  G_R2 + G_R3   1   1] [ V_R2]   =     0
[           0           -1           -1   0   0] [ I_VQ]   =   -VQ
[           1            0           -1  HM   0] [ I_HM]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4        -G_R3        -G_R3  0  -1   0] [ V_R4]   =     0
[       -G_R3  G_R1 + G_R3         G_R3  1   0   0] [ V_R1]   =     0
[       -G_R3         G_R3  G_R2 + G_R3  1   1   0] [ V_R2]   =     0
[           0           -1           -1  0   0   0] [ I_VQ]   =   -VQ
[           1            0           -1  0   0  HM] [ I_HM]   =     0
[        G_R3        -G_R3        -G_R3  0   0   1] [ I_R3]   =     0
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4            0        -G_R3  -1] [ V_R4]   =        0
[           0  G_R1 + G_R2        -G_R2  -1] [ V_R1]   =        0
[       -G_R3        -G_R2  G_R2 + G_R3   1] [ V_IQ]   =      -IQ
[           1            1           -1   0] [ I_HM]   =   -HM*IQ
    """
    return g, ctrl_src, tree, result

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

    result = """
[ G_R3 + G_R4            0        -G_R3  -1   0] [ V_R4]   =     0
[           0  G_R1 + G_R2        -G_R2  -1   0] [ V_R1]   =     0
[       -G_R3        -G_R2  G_R2 + G_R3   1   0] [ V_IQ]   =   -IQ
[           1            1           -1   0  HM] [ I_HM]   =     0
[           0        -G_R1            0   0   1] [ I_R1]   =     0
    """
    return g, ctrl_src, tree, result

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

if __name__ == '__main__':
    from sympycore import Matrix

    print '    **** Test Schnittanalyse ****'
    for test_func in tests:
        print '*', test_func.__name__
        g, ctrl_src, tree, result = test_func()
        treebrns = tree.branches()
        cobrns = g.branches() - treebrns
        eqs, vars = cut_analysis(g, ctrl_src, tree)
        A, b = create_matrices(eqs, vars)
        # pretty print of the matrix equation
        eqs_str = [str(Matrix(M)).split('\n') for M in A, vars, b]
        lines = ['[%s] [%s]   =  %s' % (e, v, r) for e, v, r in zip(*eqs_str)]
        lines = '\n'.join(lines)
        if lines != str(result).strip():
            print '  Baum', treebrns, ',  Ctrls', ctrl_src, ',  Cobaum', cobrns
            print lines
            raise Exception, 'Equations different in %s' % test_func.__name__
