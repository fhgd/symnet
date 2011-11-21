# This Python file uses the following encoding: utf-8
from pyparsing import *
from sympy import *

"""
Literatur:

* Symbolic Circuit Analysis:  http://rodanski.net/ben/work/symbolic/index.htm

Gedanken zur internen Struktur:


* Knoten:

    # Topologie
    Get-Funktion: Menge der angeschlossenen Zweige


* Zweig:

    # Topologie
    Var: (Von-Knoten, Nach-Knoten)

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

    Menge aus orientierten Zweigen, deren Knoten sowohl
    innerhalb als auch auserhalb des Schnittes liegen

    Von Knotenmenge auf Zweigmenge:
        aus der Menge aller Zweige, welche zur Knotenmenge gehören,
        diejenigen auswählen, welche einen Knoten beitzen, der
        nicht zur Knotenmenge gehört


* Masche:

    Liste von Knoten und Zweigen, die einen *geschlossenen Weg* von
    Knoten zu Knoten über Zweige angeben

    Zweig = Von-Knoten - Nach-Knoten
    Knoten - Zweig = Zweig so orientieren, dass er an Knoten anschließt
    Knoten1 - Knoten2 = Knotenspannung


* Baum:

    Ist eine Menge *nicht geschlossener Wege* im Netzwerk, die jedoch
    mit *einem* Zweig (vielleicht auch Weg) aus dem Nichtbaum
    geschlossen werden.
    (Alternativ: Eine Teilmenge von Zweigen, welche alle Knoten verbindet und
    dabei aber keine Masche bildet heisst Baum.)

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
    3. Die übrigen Knoten besitzen alle genau zwei Zweige, welche die
       Fundamentalmasche des Nichtbaumzweiges bilden.

* Fundamentalschnitt (eines Baumzweiges):

    Bei Entfernung eines Baumzweiges und entsprechender Nichtbaumzweige
    zerfällt das Netzwerk in zwei seperate Teile, so dass diese Zweige einen
    Fundamentalschnitt bilden.

    1. Alle Fundamentalmaschen aufsuchen, welche diesen Baumzweig enthalten.
    2. Die Nichtbaumzweige dieser Fundamentalmaschen gehören zum
       Fundamentalschnitt.

* Minimale Anzahl unabhaengiger Netzwerkgroessen:

    k-1 unabh. Baumspannungen (wenige Knoten, viele Zweige)
    z - (k-1) unabh. Nichtbaumstroeme (mehr Baum- als Verbindungszweige)

ToDo:
        modifizierte KSA
        Maschenströme sinnvoll definieren
        (Strom der Fundamentalmasche in Richtung des Nichtbaumzweiges?)

        Mehrpole


Nutzerinterface:


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
    matrix = zeronm(n, m+1)

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
        TYPE = oneOf('R L C I V',caseless=True)
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

if __name__ == '__main__':
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
    pprint( Symbol('V_M')==collect(together(result[VL]-result[VR]), Symbol('V1_0')) )






