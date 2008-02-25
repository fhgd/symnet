# This Python file uses the following encoding: utf-8
from pyparsing import *
from sympy import *

class zweig_element:
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

class resistor(zweig_element):
  def setup(self):
    self.param = Symbol(self.name)
  def get_u(self):
    return self.u
  def get_i(self):
    ## i = u/R
    return self.u/self.param     

class current_source(zweig_element):
  def setup(self):
    self.param = Symbol(self.name+'_0')
  def get_u(self):
    return self.u
  def get_i(self):
    ## i = i_0
    return self.param     

class voltage_source(zweig_element):
    def setup(self):
        self.param = Symbol(self.name+'_0')
    def get_u(self):
        ## u = u_0
        return self.param
    def get_i(self):
        return self.i     

class network:
  def parseNetlist(self, fname, bezugsknoten = '0'): 
    """
    Parsen der Netliste
    """
    self.relNode = bezugsknoten
    COMMENT = "*" + Optional(restOfLine)
    NAME = Word(alphanums+"_")
    TYPE = oneOf('R L C I V',caseless=True)
    ELEMENT = Combine(TYPE+NAME)
    NETLIST = Dict(ZeroOrMore( Group(ELEMENT + NAME + NAME) ))
    NETLIST.ignore(COMMENT)
    self.data = NETLIST.parseFile(fname)
    #return self.data

  def make_nodeSet(self):
    """ 
    Aus Netliste die Knotenmenge erstellen
    """
    self.knotenmenge = {}
    for zweig in self.data.keys():
      node_from = self.data[zweig][0]
      node_to   = self.data[zweig][1]
      ## Vom Zweig den Von-Knoten zur Knotenmenge hinzufügen
      self.knotenmenge[node_from] = Symbol('U_'+node_from+self.relNode)
      ## Vom Zweig den Nach-Knoten zur Knotenmenge hinzufügen
      self.knotenmenge[node_to] = Symbol('U_'+node_to+self.relNode)
    ## Bezugsknotenspannung Null setzen
    nw.knotenmenge[nw.relNode] = Real(0)

  def make_branchSet(self):
    """ 
    Aus Netliste die Zweigmenge erstellen
    """
    self.zweigmenge = {}
    for zweig in self.data.keys():
      x = zweig[0]
      node_from = self.data[zweig][0]
      node_to   = self.data[zweig][1]
      ## Instanz der Zweig-Klasse erzeugen
      if   x == 'R':
        self.zweigmenge[zweig] = resistor(zweig)
      elif x == 'I':
        self.zweigmenge[zweig] = current_source(zweig)
      elif x == 'V':
        self.zweigmenge[zweig] = voltage_source(zweig)
      else:
        self.zweigmenge[zweig] = zweig_element(zweig)
        print "Unbekanter Typ:", zweig
      ## Vom Zweig die Von-Nach-Knoten zur Knotenmenge hinzufügen
      self.zweigmenge[zweig].node_from = node_from
      self.zweigmenge[zweig].node_to = node_to

def get_matrix(eq, syms):

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
            equ = Basic.sympify(eq[i])

            content = collect(equ.expand(), syms, evaluate=False)

            for var, expr in content.iteritems():
                if isinstance(var, Symbol) and not expr.has(*syms):
                    matrix[i, index[var]] = expr
                elif isinstance(var, Basic.One) and not expr.has(*syms):
                    matrix[i, m] = -expr
                else:
                    raise "Not a linear system. Can't solve it, yet."
    return matrix


if __name__ == '__main__':
  nw = network()
  nw.parseNetlist("par.cir")
  nw.make_branchSet()
  nw.make_nodeSet()
  print "Zweigmenge:"
  zweigkeys = nw.zweigmenge.keys()
  zweigkeys.sort()
  for key in zweigkeys:
      print ' ', key, ': Param =', nw.zweigmenge[key].param

  print "Knotenmenge:"
  knotenkeys = nw.knotenmenge.keys()
  knotenkeys.sort()
  for key in knotenkeys:
      print ' ', key,': NodeVoltage =', nw.knotenmenge[key]

  ## Aufstellen der Inzidenzrelation
  inzidenz = {}
  for key in nw.knotenmenge.iterkeys():
     inzidenz[key] = []
  for key, obj in nw.zweigmenge.iteritems():
     inzidenz[obj.node_from].append( (Real(+1), key) )
     inzidenz[obj.node_to].append( (Real(-1), key) )
  print "Inzidenzrelation"
  for key, obj in inzidenz.iteritems():
    print ' ', key, ':', obj

  print "Zweigströme:"
  for key, branch in nw.zweigmenge.iteritems():
      print ' ', branch.i, '==', branch.get_i()
  
  ## Aufstellen der Maschengleichungen
  print "Zweigspannungen:"
  branch_equ = {}
  for key, branch in nw.zweigmenge.iteritems():
     branch_equ[branch.name] = \
        nw.knotenmenge[branch.node_from] - nw.knotenmenge[branch.node_to]
     print ' ', branch.u, "==", branch_equ[branch.name]

  ## Aufstellen der Knotenspannungen
  var_nodes = [sym for node, sym in nw.knotenmenge.iteritems()]
  var_nodes.remove(Real(0))
  var_nodes.sort()  

  ## Aufstellen der Knotengleichungen
  node_equ = {}
  branch_equ_rest = {}
  var_i = {}
  for node, branches in inzidenz.iteritems():
    node_equ[node] = Symbol(node)
    node_equ[node] = 0
    for sig, branch in branches:
      u = nw.zweigmenge[branch].get_u()
      i = nw.zweigmenge[branch].get_i()
      if i != nw.zweigmenge[branch].i:
        node_equ[node] += sig*i.subs(u, branch_equ[branch])
      else:
        node_equ[node] += sig*i
        ## extra Maschengleichung übernehmen
        branch_equ_rest[branch] = branch_equ[branch] - u
        var_i[i] = None
  
  ### Aufstellen der Zustandsvariablen
  var_state = var_nodes + var_i.keys()
  print 'Zustandsvariablen:', var_state

  ### Aufstellen der Quellvariablen
  var_source = []
  for name, branch in nw.zweigmenge.iteritems():
	if name[0] == 'I' or name[0] == 'V':
		var_source.append(branch.param)

  ### Lösen der Zustandsgleichungen
  # Knotengleichung des Bezugsknoten verwerfen
  node_equ.pop(nw.relNode)
  equ_key = node_equ.keys()
  equ_key.sort()
  equation = []
  for node in equ_key:
    equation.append(node_equ[node].expand())
    print 'Knoten', node, ':', node_equ[node].expand()
  
  for branch, equ in branch_equ_rest.iteritems():
    equation.append(equ.expand())
    print 'Masche', branch, ':', equ
  C = get_matrix(equation, var_state)
  A=C[:,:-1]
  B=C[:,-1]
  print 'Matrix A :'
  print A
  print 'Matrix B :'
  print B
  print ''

  det = A.det()
  pprint(Symbol('det A =') == together(det))
  print ''

  det_var = {}
  for i in range(len(var_state)):
    A[:,i] = B
    det_var[var_state[i]] = A.det()
	#det_var[var_state[i]] = collect(A.det(), var_source)
    A=C[:,:-1]
  print 'Hallo'
  result = {}
  for var in var_state:
    result[var] = collect(together((det_var[var] / det).expand()), var_source)
	#result[var] = together(collect((det_var[var] / det).expand(), var_source))
    pprint(var == result[var])
    print ''





