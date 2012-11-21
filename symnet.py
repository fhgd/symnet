# This Python file uses the following encoding: utf-8

from sympycore import Calculus

class Graph(object):
    def __init__(self, name=''):
        """The graph contain branches between nodes"""
        self.node_in = {}
        self.node_out = {}
        self.branches_in = {}
        self.branches_out = {}
        self.name = name

    def add_branch(self, branch, n1, n2):
        """Add a new branch to the graph"""
        self.node_in[branch] = n1
        self.node_out[branch] = n2

        if n2 not in self.branches_in:
            self.branches_in[n2] = set()
        self.branches_in[n2].add(branch)

        if n1 not in self.branches_out:
            self.branches_out[n1] = set()
        self.branches_out[n1].add(branch)

    def nodes(self, branch=None):
        """Return the two nodes of branch or all nodes of the graph"""
        if branch:
            return self.node_in[branch], self.node_out[branch]
        else:
            return set(self.branches_in) | set(self.branches_out)

    def branches(self, node=None):
        """Return all connecting branches to node or all branches of the graph"""
        if node:
            return self.branches_in.get(node, set()) | self.branches_out.get(node, set())
        else:
            return set(self.node_in) | set(self.node_out)

    def tree(self, branches):
        """Return the graph of branches if branches are a tree"""
        if len(branches) == len(self.nodes()) - 1:
            tree = Graph()
            for branch in branches:
                tree.add_branch(branch, *self.nodes(branch))
            if tree.nodes() == self.nodes():
                return tree
            else:
                raise Exception, 'Tree does not contain all nodes'
        else:
            raise Exception, 'Tree does not contain %i - 1 branches.' % len(self.nodes())

    def _neighbors(self, branch, node):
        """Return recursively all nodes connected to branch on the node side"""
        branches = self.branches(node)
        branches.remove(branch)
        result = set([node])
        for br in branches:
            other_node = set(self.nodes(br))
            other_node.remove(node)
            result.update(self._neighbors(br, other_node.pop()))
        return result

    def cut(self, tb, tree, include_tree_branch=True):
        """Return all branches from the cut with the tree branch tb"""
        bin = set()
        bout = set()
        for node in tree._neighbors(tb, tree.node_in[tb]):
            bin.update(self.branches_in.get(node, set()))
            bout.update(self.branches_out.get(node, set()))
        if not include_tree_branch:
            bout.remove(tb)
        bpos = bout - bin
        bneg = bin - bout
        return bpos, bneg

    def loop(self, cb, tree, include_cobranch=False):
        """Return all branches from the loop through the cobranch cb"""
        lpos = set()
        lneg = set()
        for tb in tree.branches():
            bpos, bneg = self.cut(tb, tree)
            if cb in bpos:
                # if branches cb and tb have the same cut direction
                # then they must have the opposit loop direction
                lneg.add(tb)
            if cb in bneg:
                lpos.add(tb)
        if include_cobranch:
            lpos.add(cb)
        return lpos, lneg

def f_u(brn, ctrl_src):
    """Return the voltage of branch brn"""
    type = brn[0]
    if type == 'R':
        return brn+'*I_'+brn
    elif type == 'H':
        return brn+'*'+branch_current(ctrl_src[brn], ctrl_src)
    elif type == 'E':
        return brn+'*'+branch_voltage(ctrl_src[brn], ctrl_src)
    elif type == 'V':
        return brn
    else:
        return 'V_'+brn

def f_i(brn, ctrl_src):
    """Return the current of branch brn"""
    type = brn[0]
    if type == 'R':
        return 'G_'+brn+'*V_'+brn
    elif type == 'G':
        return brn+'*'+branch_voltage(ctrl_src[brn], ctrl_src)
    elif type == 'F':
        return brn+'*'+branch_current(ctrl_src[brn], ctrl_src)
    elif type == 'I':
        return brn
    else:
        return 'I_'+brn

def branch_voltage(brn, ctrl_src):
    """Return the branch voltage symbol"""
    type = brn[0]
    if type in 'V':
        return brn
    else:
        return 'V_'+brn

def branch_current(brn, ctrl_src):
    """Return the branch current symbol"""
    type = brn[0]
    if type in 'I':
        return brn
    elif type in 'G':
        return f_i(brn, ctrl_src)
    else:
        return 'I_'+brn

def cut_analysis(g, tree):
    """Cut analysis respect to the tree of the network graph g"""
    eqs = []
    vars = []
    ctrl_branches = []
    # cut equations of the tree currents
    for tb in tree.branches():
        if tb[0] not in 'V':
            bpos, bneg = g.cut(tb, tree)
            lhs_pos = [f_i(b, ctrl_src) for b in bpos]
            lhs_neg = [f_i(b, ctrl_src) for b in bneg]
            lhs = Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
            eqs.append(lhs)
            vars.append(Calculus('V_'+tb))
    covolts = {}
    for cobranch in g.branches() - tree.branches():
        lpos, lneg = g.loop(cobranch, tree)
        # moving (bpos, bneg) from lhs to rhs by negation
        rhs_pos = [branch_voltage(b, ctrl_src) for b in lneg]
        rhs_neg = [branch_voltage(b, ctrl_src) for b in lpos]
        rhs = Calculus.Add(*rhs_pos) - Calculus.Add(*rhs_neg)
        if cobranch[0] not in 'V':
            covolts[Calculus('V_'+cobranch)] = rhs
        elif cobranch[0] in 'V':
            eqs.append(Calculus(cobranch) - rhs)
            vars.append(Calculus('I_'+cobranch))
    for ctrl in ctrl_branches:
        pass
    eqs = [e.subs(covolts).expand() for e in eqs]
    return eqs, vars

def loop_analysis(g, ctrl_src, tree):
    """Loop analysis respect to the tree of the network graph g"""
    eqs = []
    vars = []
    # loop equations of the cobranch voltages
    cobranches = g.branches() - tree.branches()
    for cobranch in cobranches:
        if cobranch[0] not in 'IFG':
            lpos, lneg = g.loop(cobranch, tree, include_cobranch=True)
            lhs_pos = [f_u(b, ctrl_src) for b in lpos]
            lhs_neg = [f_u(b, ctrl_src) for b in lneg]
            lhs = Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
            eqs.append(lhs)
            vars.append(Calculus('I_'+cobranch))
    # cut equations of the tree currents (for substitution or additional)
    tcur = {}
    for tb in tree.branches():
        bpos, bneg = g.cut(tb, tree, include_tree_branch=False)
        # moving (bpos, bneg) from lhs to rhs by negation
        rhs_pos = [branch_current(b, ctrl_src) for b in bneg]
        rhs_neg = [branch_current(b, ctrl_src) for b in bpos]
        rhs = Calculus.Add(*rhs_pos) - Calculus.Add(*rhs_neg)
        if tb[0] not in 'IFG': # and tb not in ctrl_cur:
            tcur[Calculus('I_'+tb)] = rhs
        else:
            eqs.append(Calculus(f_i(tb, ctrl_src)) - rhs)
            vars.append(Calculus('V_'+tb))
    # finally add equations and variables of the control branches
    ctrl_volts = []
    ctrl_cur = []
    for src in ctrl_src:
        if src[0] in 'EG':
            ctrl_volts.append(ctrl_src[src])
        if src[0] in 'F' and src in cobranches:
            ctrl_cur.append(ctrl_src[src])
    # control currents
    for ctrl in ctrl_cur:
        i_ctrl = Calculus('I_'+ctrl)
        if ctrl[0] not in 'I' and i_ctrl not in vars:
            # control voltage is unknown
            vars.append(i_ctrl)
            if ctrl in cobranches:
                # add loop equation for control voltage
                v_ctrl = Calculus('V_'+ctrl)
                lpos, lneg = g.loop(ctrl, tree, include_cobranch=False)
                lhs_pos = [f_u(b) for b in lpos]
                lhs_neg = [f_u(b) for b in lneg]
                lhs = v_ctrl + Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
            else:
                # add cut equation for control branch
                bpos, bneg = g.cut(ctrl, tree, include_tree_branch=False)
                lhs_pos = [branch_current(b, ctrl_src) for b in bpos]
                lhs_neg = [branch_current(b, ctrl_src) for b in bneg]
                lhs = i_ctrl + Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
            eqs.append(lhs)
    # control voltages
    for ctrl in ctrl_volts:
        v_ctrl = Calculus('V_'+ctrl)
        if ctrl[0] not in 'V' and v_ctrl not in vars:
            # control voltage is unknown
            vars.append(v_ctrl)
            # try if control voltage can be substituted
            lhs = v_ctrl - f_u(ctrl, ctrl_src)
            if lhs == 0:
                if ctrl in cobranches:
                    # add loop equation for control voltage
                    lpos, lneg = g.loop(ctrl, tree, include_cobranch=False)
                    lhs_pos = [f_u(b) for b in lpos]
                    lhs_neg = [f_u(b) for b in lneg]
                    lhs = v_ctrl + Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
                else:
                    # add cut equation for control branch
                    i_ctrl = Calculus('I_'+ctrl)
                    bpos, bneg = g.cut(ctrl, tree, include_tree_branch=False)
                    lhs_pos = [branch_current(b, ctrl_src) for b in bpos]
                    lhs_neg = [branch_current(b, ctrl_src) for b in bneg]
                    lhs = i_ctrl + Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
            eqs.append(lhs)
    eqs = [e.subs(tcur).expand() for e in eqs]
    return eqs, vars

def create_matrices(eqs, vars):
    """Convert the linear equations eqs = 0 into Ax = b with x = vars"""
    # every var in vars must be unique
    # vars == set(vars)
    A, b = [], []
    vars_zero = dict((var, 0) for var in vars)
    for eq in eqs:
        line = [eq.subs(var, 1) - eq.subs(var, 0) for var in vars]
        A.append(line)
        b.append(-eq.subs(vars_zero))
    return A, b

"""
Idee zu den Zweigen:
    Statt Strings könnten die Zweige auch eigene Objekte sein (Unterklasse
    von String?), welche die benöigten Informationen bequemer bereitstellen.

        b.name
        b.type                  # auch durch Klasse erkennbar?!
        b.i
        b.u
        b.f_i
        b.f_u
        b.controlled_branch     # für gesteuerte Quellen

    Klasse muss aber *immutable* sein!

Gesteuerte Quellen:

    Alternative zur extra Klasse: steuernder Zweig mit im Namen angeben,
    zBsp.: 'G2(R3)'

v = E(v)
i = F(i)
i = G(u)
v = H(i)

    Schnittanalyse:
        I(u) keine Extrabehandlung
        I(i) Beim Einsetzen der Zweigrelationen den Steuerstrom i = f_i(u)
             mit ersetzten
        U(u) Gleichung U_branch - U(u) = 0 aufstellen und U_branch, u durch
             Baumspannungen ersetzen.
        U(i) Gleichung U_branch - U(i) = 0 aufstellen, den Steuerstrom i = f_i(u)
             ersetzen und dann U_branch und u durch Baumspannungen ersetzen.

    Maschenanalyse:
        U(i) keine Extrabehandlung
        U(u) Beim Einsetzen der Zweigrelationen die Steuerspannung u = f_u(i)
             mit ersetzten
        I(i) Gleichung I_branch - I(u) = 0 aufstellen und I_branch, i durch
             Cobaumströme ersetzen.
        I(u) Schnittgleichung I_branch - I(u) = 0 aufstellen, die Steuerspannung
             u = f_u(i) ersetzen und dann I_branch und i durch Cobaumströme
             ersetzen.
"""


if __name__ == '__main__':
    from sympycore import Matrix

    g = Graph()
    g.add_branch('VQ', 'A', '0')
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('GM', 'L', 'R')

    tree = g.tree(['R1', 'VQ', 'R4'])
    ctrl_src = {'GM' : 'R2'}

    #~ tree = g.tree(['R1', 'Iq', 'R2'])
    #~ tree = g.tree(['R1', 'R2', 'R3'])
    #~ tree = g.tree(['V1', 'Rm', 'R4'])
    #~ tree = g.tree(['V1', 'R2', 'R4'])

    print '* Maschen der Nichtbaumzweige:'
    for cobranch in g.branches() - tree.branches():
        lpos, lneg = g.loop(cobranch, tree)
        # moving (bpos, bneg) from lhs to rhs by negation
        rhs_pos = ' + '.join(['V_'+b for b in lneg])
        rhs_neg = ''.join([' - V_'+b for b in lpos])
        print 'V_'+cobranch, '=', rhs_pos+rhs_neg
    print '* Schnitte der Baumzweige:'
    for tb in tree.branches():
        bpos, bneg = g.cut(tb, tree)
        lhs_pos = ' + '.join(['I_'+b for b in bpos])
        lhs_neg = ''.join([' - I_'+b for b in bneg])
        print tb, ':', lhs_pos+lhs_neg, '= 0'
    print '* Schnittanalyse:'
    eqs, vars = cut_analysis(g, tree)
    A, b = create_matrices(eqs, vars)
    # pretty print of the matrix equation
    eqs_str = [str(Matrix(M)).split('\n') for M in A, vars, b]
    for e, v, r in zip(*eqs_str):
        print '[%s] [%s]   =  %s' % (e, v, r)
    print '* Maschenanalyse:'
    eqs, vars = loop_analysis(g, ctrl_src, tree)
    A, b = create_matrices(eqs, vars)
    # pretty print of the matrix equation
    eqs_str = [str(Matrix(M)).split('\n') for M in A, vars, b]
    for e, v, r in zip(*eqs_str):
        print '[%s] [%s]   =  %s' % (e, v, r)
    if len(eqs) > len(vars):
        print '\n!!! Zuwenig Unbekannte !!!'
    if len(eqs) < len(vars):
        print '\n!!! Zuwenig Gleichungen !!!'

"""
Literatur:

* Symbolic Circuit Analysis:  http://rodanski.net/ben/work/symbolic/index.htm

Gedanken zur internen Struktur:


* Knoten:

    # Topologie
    Get-Funktion: Menge der angeschlossenen Zweige

    nodes = {'node_name' : (set(startBranches), set(endBranches))}
    node_branches = set.union(*nodes[node])     # g.node.branches
    node_branches_start = nodes[node][0]        # g.node.branches_start
    node_branches_end   = nodes[node][1]        # g.node.branches_end

    def inverse(mydict):
        return dict((v, k) for k, vals in mydict.items() for v in vals)
        # Fehler, wenn ein Knoten nur einen Zweig enthält!
        # Bei leeren Mengen kein Fehler?!

* Zweig:

    # Topologie
    Var: (Von-Knoten, Nach-Knoten)

    branches = {'branch_name' : (from_node, to_node)}
    branch_nodes = branches[branch]             # g.branch.nodes
    branch_from_node = branches[branch][0]      # g.branch.node_from
    branch_to_node = branches[branch][1]        # g.branch.node_to

    # Netzwerkgrössen
    Var-Symbol: Zweigspannung, Zweigstrom

    # Zweigrelation
    Funktion: Bauteilinstanz (U=f(i), I=f(u), R, L, C, Norator, Fixator)

ToDo: Unterschied zwischen Zweig und Bauteil?!

    Keiner, da ein Zweig = Von-Nach-Knoten + Zweigrelation
    und ein Bauteil ja auch nur als Relation zw. I/U dargestellt wird.

    Schon alleine die benötigte Existenz von Zweig-I/U impliziert die
    Existenz zweier Knoten: Eine Spannung existiert nur zw zwei Knoten,
    Ein Strom kann nur in einem Pfad fließen, der wiederum zw zwei
    (oder mehreren) Knoten liegt.

    Bauteile mit mehr als zwei Knoten, sollten als Teilnetzwerke
    behandelt werden.

Zweigrelation:

    Als f() implementieren und dann zB:

      fU = f
      fI = solve(self.U==f, self.I)

    Ganz allgemein: f(alle Netzwerkgrößen, Parameter)

    Verallgemeinerung: mehrere Parameter, mehrere Steuergrößen verwalten

    Mehrere Definitionsgleichungen (insbesondere fU, fI) zu verwalten scheint
    nicht notwendig, da diese als hybrides System modelliert werden können.

* Schnitt:

    Menge aus innern Knoten

        cut = set(some nodes)

    Menge aus orientierten Zweigen, deren Knoten sowohl
    innerhalb als auch auserhalb des Schnittes liegen

    Von Knotenmenge auf Zweigmenge:
        aus der Menge aller Zweige, welche zur Knotenmenge gehören,
        diejenigen auswählen, welche einen Knoten beitzen, der
        nicht zur Knotenmenge gehört

        cut_branches = set()
        for node in cut:
            for branch in nodes[node]:
                for branch_node in branches[branch]:
                    if branch_node not in cut:
                        cut_branches.add(branch)

        ToDo: Schnittzweige orientieren!


    Achtung: complement(cut, nodes) ist bis auf das Vorzeiches der
             gleiche Schnitt!

    Die Definition über die Zweige scheint zweckmäßiger zu sein. (Wegen der
    Baummethoden und der benötigen Zweigströme eines Schnittes)
    Dann muss aber auch die Richtung des Schnittes über einen ausgewählten
    Zweig definiert sein!

    ToDo: Von der Zweigmenge auf die Knotenmenge!
    zBsp. über Baum, welcher nur einen Zweig der Schnitt-Zweig-Menge enthält.
    Oder diese Zweigmenge aus dem Netzwerk entfernen und (irgendwie) prüfen,
    ob es noch zusammenhängend ist (zBsp. irgendeinen Baum suchen).

    Allerdings ist die Aufteilung der Knotenmenge in zwei Teile bei Entfernung
    eines Baumzweiges sehr einfach und eindeutig. Folglich wäre eine Teilmenge
    der Knotenmenge eine (bis auf Vorzeichen) eindeutige Eingabe und als Ausgabe
    könnten die Schnittzweige recht einfach berechnet werden. Wenn man einen
    Baum zu dieser Schnitt-Knotenmenge kennt, geht es sogar noch schneller,
    weil nur die Nichtbaumzweige untersucht werden müssten.

* Masche:

    Liste von Knoten und Zweigen, die einen *geschlossenen Weg* von
    Knoten zu Knoten über Zweige angeben

        loop = list(connecting branches)
        is_loop(loop) == True if loop is closed

        def make_loop(branches):
            "Order the loop branches according to the first branch"
            Return
                [(branch1, 0), (branch2, 1), ...]
            Oder alternativ:
                   [branch1, branch2, ...], {branch1 : 1, branch2 : -1}
            Evt.: Knoten-Zweig-Relation selbst aus der branches Menge erstellen

            loop = [(branches[0], 0)}
            for branch in branches[1:]:
                last_dir = loop[-1][1]
                last_node = branches[loop[-1][0]][last_dir]
                next_branch = [br for br in nodes[last_node] if br in branches]
                if len(next_branch) == 1:
                    next_branch = next_branch[0]
                    next_branch_nodes = branches[next_branch]
                    if last_node == next_branch_nodes[0]
                        loop.append((next_branch, 0))
                    else:
                        loop.append((next_branch, 1))
                    # (0, 1) |=> (1, -1) = -2x + 1
                else:
                    # No successor branch for to_node found in the branches set
                    return []
            last_dir = loop[-1][1]
            if branches[loop[-1][0]][last_dir] == branches[loop[0][0]][0]
                return loop
            else:
                # Connecting branches are not closed
                return []

    Zweig = Von-Knoten - Nach-Knoten
    Knoten - Zweig = Zweig so orientieren, dass er an Knoten anschließt
    Knoten1 - Knoten2 = Knotenspannung


* Baum:

    Ist eine Menge *nicht geschlossener Wege* im Netzwerk, die jedoch
    mit *einem* Zweig (vielleicht auch Weg) aus dem Nichtbaum
    geschlossen werden.
    (Alternativ: Eine Teilmenge von Zweigen, welche alle Knoten verbindet und
    dabei aber keine Masche bildet heisst Baum.)

    <=> Ein Baum hat k-1 Zweige, welche alle Knoten verbinden.

        tree = set(branches)
        def is_tree(tree):
            if len(tree) == len(nodes) - 1:
                tree_nodes = set(branches[branch] for branch in tree)
                if flatten(tree_nodes) == nodes:
                    return True
                else:
                    return False
            else:
                return False

    Da ein Weg nicht notwendiger Weise ein Zweig sein muss, ist auch
    kein extra virtueller Baum nötig. Jedoch kann der Baum auf die
    Eigenschaft

        .is_virtual = True|False

    geprüft werden.


* Bezeichnung der Knotenspannungen (= Baumspannungen):

    Da der Baum der Knotenspannungen auch virtuell sein kann (KSA), lassen
    sich nicht in eindeutiger Weise die Zweigbezeichnung verwendet.

    Allerdings existiert zu jedem (viruellen) Baumzweig in eindeutiger
    Weise ein (Fundametal)-Schnitt, welcher durch die inneren Knoten
    eindeutig bestimmt ist. Somit könnten die Knotenspannungen nach den
    inneren Knoten des jeweiligen Schnittes bezeichnet werden. (Vielleicht
    zur internen Bezeichnung sinnvoll, da eindeutig.)
        Diese Bezeichnung ist möglich, aber sicherlich aufwendiger.

    Oder man verwendet die Von-Nach-Knoten der (virtuellen) Baumzweige als
    (klassische) Bezeichnung für die Knotenspannungen.
        Scheint die bessere Wahl zu sein, weil einfacher und eigentlich
        auch eindeutig.

* Cobaum (Nichtbaum):

    Ist die Komplementärmenge zum Baum bzgl. des gesamten Netzwerkes.

    Frage: Besteht der Nichtbaum nur aus 'echten' Wegen, nämlich Zweigen,
    oder können auch 'Luftwege' wie Knotenspannungen erlaubt sein?

        cotree = complement(branches, tree)

* Knotenspannungsanalyse (KSA):

    Es scheint wohl (theoretisch) einfacher zu werden, wenn die fehlenden
    Zweige im Netzwerk durch Leerläufe (Stromquellen mit I=0) ergänzt werden.
    Dann ist nämlich ein Weg immer auch ein Zweig. Die Leerlaufzweige werden
    dann mit Von-Nach-Knoten bezeichnet.

    Als Bezugsknoten entweder einen beliebigen Netzwerksknoten wählen
    (zufällig oder Benutzereingabe), oder den mit den meisten
    Anschlusszweigen (zu unterschiedlichen Knoten). Dadurch wird die Anzahl
    der zusätzlichen Leerläufe minimiert.

* Fundamentalmasche (eines Nichtbaumzweiges):

    Jedem Nichtbaumzweig ist genau eine Masche zugeordnet. Diese besteht aus
    dem Nichtbaumzweig und geeigneten Baumzweigen. Diese Baumzweige lassen
    sich wie folgt finden:

    1. Von der Knotenmenge die zwei Knoten des Nichtbaumzweiges entfernen
    2. Alle Knoten entfernen, welche nur einen Baumzweig besitzen
    3. Die übrigen Knoten besitzen noch genau zwei (Baum)-Zweige, welche die
       Fundamentalmasche des Nichtbaumzweiges bilden.

    lbranches = copy(tree)
    for node in (nodes - branches[cobranch]):
        # Wenn Schnittmenge der Knotenzweige mit Baumzweigen == 1,
        # dann ist dies ein freier Baumzweig und wird entfernt.
        trbranches = [branch for branch in nodes[node] if branch in lbranches]
        if len(trbranches) == 1:
            lbranches.remove(trbranches)
    fdloops = {cobranch1 : lbranches1, cobranch2 : lbranches2, ...}

    loop = make_loop([cobranch] + lbranches)

    Fundamentalmasche suchen würde schneller gehen, wenn der Baum ein eigenes
    Netzwerk bzw. Graph wäre.

Alternativ: Menge der Fundamentalmaschen-Baumzweige aus den Fundamentalschnitten
    bestimmen.

    # Fundamentalmasche für 'cobranch'
    loop = [trb for trb, cutbrunches in fdcuts.items() if cobranch in cutbrunches]

    ToDo: Orientierung der Baumzweige bzgl. cobranch sollte möglich sein.

* Fundamentalschnitt (eines Baumzweiges):

    Bei Entfernung eines Baumzweiges und entsprechender Nichtbaumzweige
    zerfällt das Netzwerk in zwei seperate Teile, so dass diese Zweige einen
    Fundamentalschnitt bilden.

    1. Alle Fundamentalmaschen aufsuchen, welche diesen Baumzweig enthalten.
    2. Die Nichtbaumzweige dieser Fundamentalmaschen gehören zum
       Fundamentalschnitt.

    # Fundamentalschnitt für 'trbranch'
    cutbranches = [cb for cb, lbrnches in fdloops.items() if trbrnch in lbrnches]
    fdcuts = {trbanch1 : cutbrunches1, ...}

    Allgemeiner (ohne Baum), aber aufwändiger, siehe oben bei 'Schnitt'.

* Minimale Anzahl unabhaengiger Netzwerkgroessen:

    k-1 unabh. Baumspannungen (wenige Knoten, viele Zweige)
    z - (k-1) unabh. Nichtbaumstroeme (mehr Baum- als Verbindungszweige)

    len(nodes) - 1
    len(branches) - (len(nodes) - 1)

* Algebra:
    Aus der Zweigmenge einer Masche oder Schnittes resultiert:

        i1 + i2 + ... ik = 0    bzw.    u1 + u2 + ... uk = 0

    Es sollte auch ohne CAS möglich sein, eine einzelne Zweig-U/I
    zu berechnen:

        i1 = -i2 + ... - ik     bzw.    u1 = -u2 + ... - uk

    Dies ist notwendig, damit die Ströme und Spannungen der Maschen
    und Schnitte ersetzt werden können.

    Damit sollten sich auch die Admitanzmatrizen aufstellen lassen.
    (Evt. alle Funtamentalgleichungen durchnummerieren und als Matrizen
    aufstellen? 0 = I G U0   mit I=Schnitte, G=Leitwerte, U0=Maschen)

    Damit sollten auch bei lineare NW die Knoten- bzw. Maschengleichung
    nach den Quellen auflösbar sein:

        IQ = i1 + i2 + ... ik   bzw. UQ = u1 + u2 + ... + uk

    Folglich könnte die etwas aufwändige Trennung der Variablen für das
    lineare Gleichungssystem (Matrix) entfallen.

    => Folgende Gleichungen zum 'ausrechnen' erzeugen:

        fI1(u1) + fI2(u1-u3) + fI3(u3) = Iq
        ...

    Matrix (für u1, u3) mit CAS erzeugen.

    Vielleicht wäre es aber besser, die Ersetzungen (u2 = u1-u3) auch dem
    CAS zu überlassen?!

ToDo:
        modifizierte KSA
        Maschenströme sinnvoll definieren
        (Strom der Fundamentalmasche in Richtung des Nichtbaumzweiges?)

        Mehrpole


Nutzerinterface:

   +---- R1+ -----+---+
   |              |   Y
   +---- Uq -->---+  +|
         +-           IQ
                     -|
                      A         (Verbraucherzählpfeilsystem)
                      |         (oder Standardorientierung von li-re, ob-un)
                      +----

* Eingabe:

    # leeres Netzwerk
    nw = network()

    # nur Knoten, keine Zweige
    nw = network(Knotenmenge)

    # Netzliste = Zweigmenge
    # Knotenmenge aus den Von-Nach-Knoten der einzelnen Zweige bestimmen
    nw = network(Zweigmenge)

    # Netzliste aus Datei
    nw = network('circuit.cir')
    nw.parse_netlist('circuit.cir')


* Modifikationen:

    # Sehr schön wäre ja bestimmt: (Frage Zweig-Bauteil)
    nw += zweig
    nw -= zweig
    nw += knoten
    nw -= knoten

    # Hinzufügen
    nw.add(knoten)
    nw.add(zweig) # automatisch Knoten hinzufügen

    nw.nodes.add(knoten)
    nw.branches.add(zweig)

    # Löschen
    nw.remove(knoten)
    nw.remove(zweig)

    nw.branches.remove(zweig)
    nw.nodes.remove(node) # Methode überschreiben: auch Zweige entfernen

    del nw.zweig
    del nw.knoten # löscht auch alle dazugehörigen Zweige


* Ausgabe:

    # alle Knoten als set (Knotenmenge)
    nw.nodes

    # alle Zweige als set (Zweigmenge)
    nw.branches

    # unabhängige Knotengleichungen
    len(nw.nodes) - 1

    # unabhängige Maschengleichungen
    len(nw.branches) - len(nw.nodes) + 1

    # Wenn das netzwerk aus mehreren nichtzusammenhängenden
    # Teilnetzwerken besteht: 1 <=> Anzahl der Teilnetzwerke

    # Quellen mit f(0) != 0 ausgeben
    nw.i.sources
    nw.u.sources
    nw.sources

    # Lösung für eine Netzwerkgrösse = func(Quellen)
    nw.i.zweig
    nw.u.zweig

    nw.u.knoten == u_knoten + konst
    nw.u.knoten1.knoten2 == u_knoten1 - u_knoten2
    nw.relnode = bezugsknoten
    nw.u.knoten == u_knoten - u_relnode

    # oder auch
    nw.u(zweig)
    nw.u(knoten)
    nw.u(Von-Knoten, Nach-Knoten)

    # Analyse für Zweiggrössen (nw.u, nw.i) festlegen
    nw.analyse = nodal
    nw.analyse() == Liste der knotenspannungen

"""
class node2(object):
    def __init__(self, name):
        # Name nur zur leserlichen Ausgabe verwenden,
        # sonst versuchen, nur über das Objekt (Knoten)
        # selbst zuzugreifen
        self.name = name

    def get_branches(self, branches):
        pass
        """
        node_branches = set()
        for branch in branches:
            if self in branch.nodes:
                node_branches.add(branch)
        return node_branches
        """
        # Frage: ist wegen nw.branches das Netzwerk eine
        # Unterklassen von Knoten oder
        # ist ein Knoten eine Unterklasse vom Netzwerk?
        # Oder sollte get_branches(node) lieber als Methode des Netzwerks
        # definiert werden?

class branch2(object):
    def __init__(self, name):
        self.name = name
        self.V = Symbol('V_'+self.name)
        self.I = Symbol('I_'+self.name)
        self.param = Symbol(self.name)

        self.nodes = None, None
        self.node1 = property(lambda self: self.nodes[0])
        self.node2 = property(lambda self: self.nodes[1])

class resistor2(branch2):
    def fV(self):
        # V = I*R
        return self.I*self.param
    def fI(self):
        # I = U/R
        return self.V/self.param

class conductance2(branch2):
    """
    Leitwert vielleicht auch als spannungsabhängige Stromquelle?
    """
    def fV(self):
        # V = I/G
        return self.I/self.param
    def fI(self):
        # I = U*G
        return self.V*self.param

class current2(branch2):
    def fI(self):
        ## I = I_0
        return self.param

class dcurrent2(current2):
    def __init__(self, name, control):
        super(dcurrent2, self).__init__(name)
        self.control = control
    def fI(self):
        ## I = param * network variable
        return self.param * self.control

class voltage2(branch2):
    def fV(self):
        ## V = V_0
        return self.param

class dvoltage2(branch2):
    def __init__(self, name, control):
        super(dvoltage2, self).__init__(name)
        self.control = control
    def fV(self):
        ## U = param * network variable
        return self.param * self.control

class fixator2(branch2):
    def __init__(self, name):
        super(dvoltage2, self).__init__(name)
        del self.param
        self.v0 = Symbol('V_0'+self.name)
        self.i0 = Symbol('I_0'+self.name)
    def fV(self):
        return self.v0
    def fI(self):
        return self.i0

class nullator2(branch2):
    def fV(self):
        return 0
    def fI(self):
        return 0

class norator2(branch2):
    pass

class branch_element:
    def __init__(self, name):
        self.name = name
        self.type = self.name[0]
        self.node_from = None
        self.node_to = None
        self.u = Symbol('U_'+self.name)
        self.i = Symbol('I_'+self.name)
        self.setup()

    def setup(self):
        self.param = None

    def __str__(self):
        return self.name

class resistor(branch_element):
    def setup(self):
        self.param = Symbol(self.name)
    def get_u(self):
        return self.u
    def get_i(self):
        ## I = U/R
        return self.u/self.param

class conductance(branch_element):
    def setup(self):
        self.param = Symbol(self.name)
    def get_u(self):
        return self.u
    def get_i(self):
        ## I = G*U
        return self.param*self.u

class current_source(branch_element):
    def setup(self):
        self.param = Symbol(self.name+'_0')
    def get_u(self):
        return self.u
    def get_i(self):
        ## I = I_0
        return self.param

class voltage_source(branch_element):
    def setup(self):
        self.param = Symbol(self.name+'_0')
    def get_u(self):
        ## U = U_0
        return self.param
    def get_i(self):
        return self.i

class node:
    def __init__(self, name):
        self.name = name
        self.v = Symbol('V_'+self.name+'0')
        self.branches = []

def get_matrix(eq, syms):
    """
    Copy from "def solve(...)" in sympy/solvers/solvers.py
    """
    if isinstance(syms, Basic):
        syms = [syms]

    # augmented matrix
    n, m = len(eq), len(syms)
    matrix = zeros((n, m+1))

    index = {}

    for i in range(0, m):
        index[syms[i]] = i

    for i in range(0, n):
        if isinstance(eq[i], Equality):
            # got equation, so move all the
            # terms to the left hand side
            equ = eq[i].lhs - eq[i].rhs
        else:
            equ = sympify(eq[i])

            content = collect(equ.expand(), syms, evaluate=False)

            for var, expr in content.iteritems():
                if isinstance(var, Symbol) and not expr.has(*syms):
                    matrix[i, index[var]] = expr
                elif (var is S.One) and not expr.has(*syms):
                    matrix[i, m] = -expr
                else:
                    raise "Not a linear system. Can't solve it, yet."
    return matrix

class network:
    def parseNetlist(self, fname, gnd = '0'):
        """
        Parse the Netlist
        """
        self.gnd_name = gnd
        COMMENT = "*" + Optional(restOfLine)
        NAME = Word(alphanums+"_")
        TYPE = oneOf('R G L C I V',caseless=True)
        ELEMENT = Combine(TYPE+NAME)
        NETLIST = Dict(ZeroOrMore( Group(ELEMENT + NAME + NAME) ))
        NETLIST.ignore(COMMENT)
        self.data = NETLIST.parseFile(fname)

    def make_nodeSet(self):
        """
        Make NodeSet from Netlist
        """
        self.nodeSet = {}
        for branch in self.data.keys():
            node_from, node_to = self.data[branch][:]
            self.nodeSet[node_from] = node(node_from)
            self.nodeSet[node_to] = node(node_to)
        ## Set the GND-Node to Zero
        self.gnd_node = node(self.gnd_name)
        self.gnd_node.v = Real(0)
        self.nodeSet[self.gnd_name] = self.gnd_node

    def make_branchSet(self):
        """
        Make branchSet from Netlist
        """
        self.branchSet = {}
        for branch in self.data.keys():
            node_from, node_to = self.data[branch][:]
            ## first Letter of the name is the element-type
            element = branch[0]
            ## Make instance of the right branch-class
            if element == 'R':
                self.branchSet[branch] = resistor(branch)
            elif element == 'G':
                self.branchSet[branch] = conductance(branch)
            elif element == 'I':
                self.branchSet[branch] = current_source(branch)
            elif element == 'V':
                self.branchSet[branch] = voltage_source(branch)
            else:
                self.branchSet[branch] = branch_element(branch)
                print "Unknown Typ:", branch

            self.branchSet[branch].node_from = self.nodeSet[node_from]
            self.branchSet[branch].node_to = self.nodeSet[node_to]

    def make_incidence(self):
        """
        Make the incidence relation
        """
        for key, branch in self.branchSet.iteritems():
            self.nodeSet[branch.node_from.name].branches.append( (Real(+1), branch) )
            self.nodeSet[branch.node_to.name].branches.append( (Real(-1), branch) )

    def make_branchVoltages(self):
        """
        Make the branch voltages from the loop equations
        """
        branchVoltages = {}
        for key, branch in self.branchSet.iteritems():
            branchVoltages[branch.name] = \
                self.nodeSet[branch.node_from.name].v - self.nodeSet[branch.node_to.name].v
        self.branchVoltages = branchVoltages

    def make_nodeVoltages(self):
        """
        Make the node-Voltages
        """
        self.var_nodes = [sym for node, sym in self.nodeSet.iteritems()]
        self.var_nodes.remove(self.gnd_node)
        self.var_nodes.sort()
        #self.var_nodes = var_nodes

    def make_nodeEqu(self):
        """
        Make the node equations
        """
        node_equ = {}
        branch_equ = {}
        var_i = {}

        for key, node in self.nodeSet.iteritems():
            node_equ[node.name] = Real(0)
            for sig, branch in node.branches:
                u = branch.get_u()
                i = branch.get_i()
                u_loop = self.branchVoltages[branch.name]
                if i is not branch.i:
                    node_equ[node.name] += sig*i.subs(u, u_loop)
                else:
                    node_equ[node.name] += sig*i
                    branch_equ[branch.name] = u_loop - u
                    var_i[i] = None

        self.node_equ = node_equ
        self.branch_equ = branch_equ
        self.var_i = var_i


    def make_stateVar(self):
        self.var_state = [var.v for var in self.var_nodes]
        for var in self.var_i.keys():
            self.var_state.append(var)

    def make_sourceVar(self):
        var_source = []
        for name, branch in self.branchSet.iteritems():
            if name[0] == 'I' or name[0] == 'V':
                var_source.append(branch.param)
        self.var_source = var_source

    def solve(self, vars):
        """
        Solve the state equations
        """
        ## delete the equation for the gnd node
        self.node_equ.pop(self.gnd_name)
        equ_key = self.node_equ.keys()
        equ_key.sort()
        equation = []
        ## get all node equations
        for node in equ_key:
            equation.append(nw.node_equ[node].expand())
        ## get all loop equations
        for branch, equ in self.branch_equ.iteritems():
            equation.append(equ.expand())
        self.equation = equation

        C = get_matrix(self.equation, self.var_state)
        ## get the lhs matrix (coefficient matrix)
        A=C[:,:-1]
        print A
        ## get the rhs matrix
        B=C[:,-1]
        self.C = C
        self.A = A
        self.B = B
        det = A.det()

        det_var = {}
        for v in vars:
            i = self.var_state.index(v)  # position of v in var_state
            A[:,i] = B # put the lhs column to the i-column of the rhs matrix
            det_var[self.var_state[i]] = A.det()
            #det_var[var_state[i]] = collect(A.det(), var_source)
            A=C[:,:-1] # restore the rhs matrix

        result = {}
        for v in vars:
            result[v] = collect(together((det_var[v] / det).expand()), self.var_source)
        return result

#~ if __name__ == '__main__':
if False:
    from pyparsing import *
    from sympy import *

    nw = network()
    #nw.parseNetlist("par.cir")
    nw.parseNetlist("bridge.cir")
    nw.make_nodeSet()
    nw.make_branchSet()
    nw.make_incidence()
    nw.make_branchVoltages()
    nw.make_nodeVoltages()
    nw.make_nodeEqu()
    nw.make_stateVar()
    nw.make_sourceVar()

    print "branch set:"
    branchkeys = nw.branchSet.keys()
    branchkeys.sort()
    for key in branchkeys:
        print ' ', key, ': Param =', nw.branchSet[key].param

    print "node set:"
    nodeKeys = nw.nodeSet.keys()
    nodeKeys.sort()
    for key in nodeKeys:
        print ' ', key,': NodeVoltage =', nw.nodeSet[key].v

    print "branch currents:"
    for key, branch in nw.branchSet.iteritems():
        print ' ', branch.i, '==', branch.get_i()

    print "branch voltages:"
    branch_equ = {}
    for key, branch in nw.branchVoltages.iteritems():
        print ' ', key, "==", branch

    print 'state variables:', nw.var_state
    print ''

    VL=Symbol('V_L0')
    VR=Symbol('V_R0')
    result=nw.solve([VL, VR])
    #~ pprint( Eq(Symbol('V_M'), collect(together(result[VL]-result[VR]), Symbol('V1_0'))) )
    pprint( Eq(Symbol('V_L'), collect(together(result[VL]), Symbol('V1_0'))) )






