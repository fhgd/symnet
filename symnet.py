from sympycore import Calculus
import pyparsing as parse

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

