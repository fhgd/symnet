# This Python file uses the following encoding: utf-8

"""
==== Vorschlag von Daniel Schillinger:

* symnet nur (zunaechst) nur zum Aufstellen des (nichtlin.) GlSys. verwenden

(2.) Einlesen aus Netzliste
    Netzliste von: LTSpice, Qucs, SpicyVoltSim, CircuitLabs
    Frage: Wie mit gesteuerten Quellen umgehen?
        Steuergröße kann nicht nur ein anderer Zweig, sondern allgemein auch
        ein Leerlauf oder Kurzschluss sein
        (beim Einlesen einer (Spice-) Netzliste automatisch einfuegen)

(3.) Transistor als 3-Pol unterstuetzen und als einfaches Model ersetzen

(1.) Standardbaum der KSA
    automatisch Leerläufe einfügen, um die gewoehnlichen Knotenspannungen
    zu erhalten

* Gleichungen von Mathematica lösen lassen (Copy-Paste)

* Eigene grafische Eingabe
    ipython Notebook? 
    Darstellung des Netzwerkes zunaechst mit 
        - graphviz: pygraphviz, pydot
        - networkx (Node positioning algorithms) und matplotlib


==== ToDo before release:

* Standardbaum der KSA (automatisch Leerläufe einfügen)

* Beispiele

* Trivialgleichungen wenn möglich reduzieren

* Versuch: Zweigvariablen der Quellen erst später ersetzten
    Gesteuerten Quellen zuerst wie unabhängige Quellen behandeln, dann
    erst ersetzten...

    Damit rekursive Struktur von branch_{current,voltage} und f_{i,u} entfernen

* CleanUp

* Lösen des lin. Gl.Sys. mit sympycore?
"""

from sympycore import Calculus

class Graph(object):
    def __init__(self, incidence={}, name=''):
        """The graph is given by a incidence relation {branch: (n1, n2)}"""
        self.branches_in = {}
        self.branches_out = {}
        self.inc = {}
        for branch, nodes in incidence.items():
            self.add_branch(branch, *nodes)
        self.name = name

    def __repr__(self):
        return 'Graph(%s)' % repr(self.inc)

    def add_branch(self, branch, n1, n2):
        """Add a new branch from node n1 to node n2 to the graph"""
        self.inc[branch] = n1, n2

        if n2 not in self.branches_in:
            self.branches_in[n2] = set()
        self.branches_in[n2].add(branch)

        if n1 not in self.branches_out:
            self.branches_out[n1] = set()
        self.branches_out[n1].add(branch)

    def pop_branch(self, branch):
        """Remove branch from graph and return branch nodes"""
        n1, n2 = self.inc.pop(branch)
        self.branches_in[n2].remove(branch)
        if not self.branches_in[n2]:
            del self.branches_in[n2]
        self.branches_out[n1].remove(branch)
        if not self.branches_out[n1]:
            del self.branches_out[n1]
        return n1, n2

    def remove_branch(self, branch):
        """Remove branch from the graph"""
        self.pop_branch(branch)

    def replace_branch(self, old, new):
        """Replace old branch by new branch"""
        try:
            nodes = self.pop_branch(old)
            self.add_branch(new, *nodes)
        except KeyError:
            pass

    def nodes(self, branch=None):
        """Return the two nodes of branch or all nodes of the graph"""
        if branch:
            return self.inc[branch]
        else:
            return set(self.branches_in) | set(self.branches_out)

    def branches(self, node=None):
        """Return all connecting branches to node or all branches of the graph"""
        if node:
            return self.branches_in.get(node, set()) | self.branches_out.get(node, set())
        else:
            return set(self.inc) | set(self.inc)    # preserve old order

    def node_in(self, branch):
        """Return the first node of branch"""
        return self.inc[branch][0]

    def node_out(self, branch):
        """Return the second node of branch"""
        return self.inc[branch][1]

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
        for node in tree._neighbors(tb, tree.node_in(tb)):
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

def btype(brn, types):
    return types.get(brn, brn[0])

def bindex(brn, types):
    if brn in types:
        return brn
        return '_'+brn
    else:
        return brn[1:]

def f_u(brn, ctrl_src, types):
    """Return the voltage of branch brn"""
    type = btype(brn, types)
    if type == 'R':     # u = R i
        return brn+'*I_'+brn
    elif type == 'H':   # u = H i_ctrl
        return brn+'*'+branch_current(ctrl_src[brn], ctrl_src, types)
    elif type == 'E':   # u = E u_ctrl
        return brn+'*'+branch_voltage(ctrl_src[brn], ctrl_src, types)
    elif type == 'V':   # u = V
        return 'V'+bindex(brn, types)
    else:               # u = V_brn
        return 'V_'+brn

def f_i(brn, ctrl_src, types):
    """Return the current of branch brn"""
    type = btype(brn, types)
    if type == 'R':     # i = G_R u
        return 'G_'+brn+'*V_'+brn
    elif type == 'G':   # i = G u_ctrl
        return brn+'*'+branch_voltage(ctrl_src[brn], ctrl_src, types)
    elif type == 'F':   # i = F i_ctrl
        return brn+'*'+branch_current(ctrl_src[brn], ctrl_src, types)
    elif type == 'I':   # i = I
        return 'I'+bindex(brn, types)
    else:               # i = I_brn
        return 'I_'+brn

def branch_voltage(brn, ctrl_src, types):
    """Return the branch voltage symbol"""
    type = btype(brn, types)
    if type in 'V':
        return 'V'+bindex(brn, types)
    elif type in 'E':
        return f_u(brn, ctrl_src, types)
    elif type in 'H':
        return f_u(brn, ctrl_src, types)
    else:
        return 'V_'+brn

def branch_current(brn, ctrl_src, types):
    """Return the branch current symbol"""
    type = btype(brn, types)
    if type in 'I':
        return 'I'+bindex(brn, types)
    elif type in 'F':
        return f_i(brn, ctrl_src, types)
    elif type in 'G':
        return f_i(brn, ctrl_src, types)
    else:
        return 'I_'+brn

def cut_analysis(g, ctrl_src, tree, types={}):
    """Cut analysis respect to the tree of the network graph g"""
    eqs = []
    vars = []

    # cut equations of the tree currents
    for tb in tree.branches():
        if btype(tb, types) not in 'VEH':
            bpos, bneg = g.cut(tb, tree)
            lhs_pos = [f_i(b, ctrl_src, types) for b in bpos]
            lhs_neg = [f_i(b, ctrl_src, types) for b in bneg]
            lhs = Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
            eqs.append(lhs)
            vars.append(Calculus('V_'+tb))

    # loop equations of the cobranch voltages
    cobranches = g.branches() - tree.branches()
    covolts = {}
    for cobranch in cobranches:
        lpos, lneg = g.loop(cobranch, tree)
        # moving (bpos, bneg) from lhs to rhs by negation
        rhs_pos = [branch_voltage(b, ctrl_src, types) for b in lneg]
        rhs_neg = [branch_voltage(b, ctrl_src, types) for b in lpos]
        rhs = Calculus.Add(*rhs_pos) - Calculus.Add(*rhs_neg)
        if btype(cobranch, types) not in 'VEH':
            covolts[Calculus('V_'+cobranch)] = rhs
        else:
            eqs.append(Calculus(f_u(cobranch, ctrl_src, types)) - rhs)
            vars.append(Calculus('I_'+cobranch))

    # finally add variables and equations of controlled sources
    for src, ctrl in ctrl_src.items():
        if btype(src, types) in 'FH' and btype(ctrl, types) != 'I':
            i_ctrl = Calculus('I_'+ctrl)
            if i_ctrl not in vars:      # ctrl is no 'VEH' in cotree
                # control current is unknown
                vars.append(i_ctrl)
                # try if control current can be substituted
                # then control branch is a (controlled) current source
                lhs = i_ctrl - f_i(ctrl, ctrl_src, types)
                if lhs == 0:
                    # ctrl is a voltage source
                    if ctrl in tree.branches():
                        # add missing cut equation for i_ctrl which
                        # was omitted due to: btype(tb, types) not in 'VEH'
                        bpos, bneg = g.cut(ctrl, tree, include_tree_branch=False)
                        lhs_pos = [f_i(b, ctrl_src, types) for b in bpos]
                        lhs_neg = [f_i(b, ctrl_src, types) for b in bneg]
                        lhs = i_ctrl + Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
                    # if i_ctrl is in cotree then var and loop equation are
                    # already added because ctrl is a voltage source
                eqs.append(lhs)
        elif btype(src, types) in 'E' and src in tree.branches():
            if ctrl in cobranches and btype(ctrl, types) not in 'VEH':
                v_ctrl = Calculus('V_'+ctrl)
                # just a test avoiding duplication
                if v_ctrl not in vars:
                    # control voltage is unknown
                    vars.append(v_ctrl)
                    # remove loop equation for ctrl from covolts and add to eqs
                    eqs.append(v_ctrl - covolts.pop(v_ctrl))

    # substitute cobranch voltages by tree voltages
    eqs = [e.subs(covolts).normal().expand() for e in eqs]
    return eqs, vars

def loop_analysis(g, ctrl_src, tree, types={}):
    """Loop analysis respect to the tree of the network graph g"""
    eqs = []
    vars = []

    # loop equations of the cobranch voltages
    cobranches = g.branches() - tree.branches()
    for cobranch in cobranches:
        if btype(cobranch, types) not in 'IFG':
            lpos, lneg = g.loop(cobranch, tree, include_cobranch=True)
            lhs_pos = [f_u(b, ctrl_src, types) for b in lpos]
            lhs_neg = [f_u(b, ctrl_src, types) for b in lneg]
            lhs = Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
            eqs.append(lhs)
            vars.append(Calculus('I_'+cobranch))

    # cut equations of the tree currents (for substitution or additional)
    tcur = {}
    for tb in tree.branches():
        bpos, bneg = g.cut(tb, tree, include_tree_branch=False)
        # moving (bpos, bneg) from lhs to rhs by negation
        rhs_pos = [branch_current(b, ctrl_src, types) for b in bneg]
        rhs_neg = [branch_current(b, ctrl_src, types) for b in bpos]
        rhs = Calculus.Add(*rhs_pos) - Calculus.Add(*rhs_neg)
        if btype(tb, types) not in 'IFG':
            tcur[Calculus('I_'+tb)] = rhs.expand()
        else:
            eqs.append(Calculus(f_i(tb, ctrl_src, types)) - rhs)
            vars.append(Calculus('V_'+tb))

    # finally add variables and equations of controlled sources
    for src, ctrl in ctrl_src.items():
        if btype(src, types) in 'EG' and btype(ctrl, types) != 'V':
            v_ctrl = Calculus('V_'+ctrl)
            if v_ctrl not in vars:      # ctrl is no 'IFG' in tree
                # control voltage is unknown
                vars.append(v_ctrl)
                # try if control voltage can be substituted
                # then control branch is a (controlled) voltage source
                lhs = v_ctrl - f_u(ctrl, ctrl_src, types)
                if lhs == 0:
                    # ctrl is a current source
                    if ctrl in cobranches:
                        # add missing loop equation for v_ctrl which
                        # was omitted due to: btype(cobranch, types) not in 'IFG'
                        lpos, lneg = g.loop(ctrl, tree, include_cobranch=False)
                        lhs_pos = [f_u(b, ctrl_src, types) for b in lpos]
                        lhs_neg = [f_u(b, ctrl_src, types) for b in lneg]
                        lhs = v_ctrl + Calculus.Add(*lhs_pos) - Calculus.Add(*lhs_neg)
                    # if v_ctrl is in tree then var and cut equation are
                    # already added because ctrl is a current source
                eqs.append(lhs)
        elif btype(src, types) in 'F' and src in cobranches:
            if ctrl in tree.branches() and btype(ctrl, types) not in 'IFG':
                i_ctrl = Calculus('I_'+ctrl)
                # just a test avoiding duplication
                if i_ctrl not in vars:
                    # control current is unknown
                    vars.append(i_ctrl)
                    # remove cut equation for ctrl from tcur and add it to eqs
                    eqs.append(i_ctrl - tcur.pop(i_ctrl))

    # substitute tree currents by cobranch currents
    eqs = [e.subs(tcur).expand() for e in eqs]
    return eqs, vars

def create_matrices(eqs, vars):
    """Convert the linear equations eqs = 0 into Ax = b with x = vars"""
    if len(vars) > len(set(vars)):
        raise Exception, 'Every var in vars must be unique!'
    A, b = [], []
    vars_zero = dict((var, 0) for var in vars)
    for eq in eqs:
        line = [eq.subs(var, 1) - eq.subs(var, 0) for var in vars]
        A.append(line)
        b.append(-eq.subs(vars_zero))
    return A, b

def parse_netlist(netlist='', types={}):
    """Return graph and controlled sources dictionary of netlist"""
    import pyparsing as parse
    COMMENT = "*" + parse.Optional(parse.restOfLine)
    NAME = parse.Word(parse.alphanums+"_")
    TYPE = parse.oneOf('R V I E F G H', caseless=True)
    ELEMENT = parse.Combine(TYPE+NAME)
    LINE = ELEMENT + NAME + NAME  + parse.Optional(~parse.LineEnd() + NAME)
    NETLIST = parse.Dict(parse.ZeroOrMore(parse.Group(LINE)))
    NETLIST.ignore(COMMENT)
    graph = {}
    ctrl_src = {}
    for brn, vals in NETLIST.parseString(netlist).items():
        graph[brn] = vals[:2]
        if btype(brn, types) in 'EFGH':
            ctrl_src[brn] = vals[2]
    return Graph(graph), ctrl_src

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

    Nicht so gut, da somit der Typ eines Zweiges nich einfach geändert
    werden kann. Besser sind dicts:

        type = types[branch]
        ctrl = ctrls[branch]

Diese beiden dicts zusammen mit dem Graphen als Netzwerk Klasse?!

Gesteuerte Quellen:

    Alternative zur extra Klasse: steuernder Zweig mit im Namen angeben,
    zBsp.: 'G2(R3)'

u = E(u)
i = F(i)
i = G(u)
u = H(i)

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

Nullator:

    Schnittanalyse:
        Wenn Nullator im Baum, dann keine Schnittgleichung aufstellen (v = 0)
                     ... Cobaum, dann liefert f_i = 0.

        Maschengleichung:
            Wenn Nullator im Cobaum, dann liefert f_u = 0 und I_cobranch NICHT
            an vars anhaengen, da wegen f_i = 0 nicht benoetigt!

            Wenn Nullator im Baum, dann liefert branch_voltage = 0.

Norator:

    Es sollte keine Extrabehandlung notwenig sein, da von f_u,i und
    branch_voltage,current bereits abgedeckt: 'I_'+brn und 'V_'+brn

    An geeigneter Stelle noch: vars.append(v_norator, i_norator)
"""

if __name__ == '__main__':
    from sympycore import Matrix

    g = Graph()
    g.add_branch('VQ', 'A', '0')
    g.add_branch('R1', 'A', 'L')
    g.add_branch('R2', 'L', '0')
    g.add_branch('R3', 'A', 'R')
    g.add_branch('R4', 'R', '0')
    g.add_branch('FM', 'L', 'R')

    tree = g.tree(['R1', 'R2', 'R4'])
    ctrl_src = {'FM' : 'R4'}

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
    eqs, vars = cut_analysis(g, ctrl_src, tree)
    A, b = create_matrices(eqs, vars)
    # pretty print of the matrix equation
    eqs_str = [str(Matrix(M)).split('\n') for M in A, vars, b]
    for e, v, r in zip(*eqs_str):
        print '[%s] [%s]   =  %s' % (e, v, r)
    if len(eqs) > len(vars):
        print '\n!!! Zuwenig Unbekannte !!!'
    if len(eqs) < len(vars):
        print '\n!!! Zuwenig Gleichungen !!!'
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

