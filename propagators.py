#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

'''
This file will contain different constraint propagators to be used within
bt_search.

propagator == a function with the following template
    propagator(csp, newly_instantiated_variable=None)
        ==> returns (True/False, [(Variable, Value), (Variable, Value) ...])

    csp is a CSP object---the propagator can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    newly_instaniated_variable is an optional argument.
    if newly_instantiated_variable is not None:
        then newly_instantiated_variable is the most
        recently assigned variable of the search.
    else:
        propagator is called before any assignments are made
        in which case it must decide what processing to do
        prior to any variables being assigned. SEE BELOW

    The propagator returns True/False and a list of (Variable, Value) pairs.

    Returns False if a deadend has been detected by the propagator.
        in this case bt_search will backtrack
    Returns True if we can continue.

    The list of variable values pairs are all of the values
    the propagator pruned (using the variable's prune_value method).
    bt_search NEEDS to know this in order to correctly restore these
    values when it undoes a variable assignment.

    NOTE propagator SHOULD NOT prune a value that has already been
    pruned! Nor should it prune a value twice

    PROPAGATOR called with newly_instantiated_variable = None
        PROCESSING REQUIRED:
            for plain backtracking (where we only check fully instantiated
            constraints) we do nothing...return (true, [])

            for forward checking (where we only check constraints with one
            remaining variable) we look for unary constraints of the csp
            (constraints whose scope contains only one variable) and we
            forward_check these constraints.

            for gac we establish initial GAC by initializing the GAC queue with
            all constaints of the csp

    PROPAGATOR called with newly_instantiated_variable = a variable V
        PROCESSING REQUIRED:
            for plain backtracking we check all constraints with V (see csp
            method get_cons_with_var) that are fully assigned.

            for forward checking we forward check all constraints with V that
            have one unassigned variable left

            for gac we initialize the GAC queue with all constraints containing
            V.
'''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    single = []
    prune = []

    constraints = csp.get_all_cons()
    if newVar != None:
        constraints = csp.get_cons_with_var(newVar)

    # print contraints #for testing
    # print("Single", single)

    # if single == []:
    #     print("single", '[]')
    # else:
    #     for s in single:
    #         print("single", s)
    single = single_constraints_FC(constraints)


    while len(single) > 0:
        # take first element of single constraint row
        constraint, unassigned = single.pop(0)
        # find domain
        cur_dom = unassigned.cur_domain()

        for item in cur_dom:

            temp = []

            for i in constraint.get_scope():
                #append assigned value if assigned

                if i != unassigned:
                    temp.append(i.get_assigned_value())

                else:
                    temp.append(item)

            if not constraint.check(temp):
                # prune
                prune.append((unassigned, item))
                unassigned.prune_value(item)

                if len(unassigned.cur_domain()) == 0: 
                    # if length is 0 then return false
                    return (False, prune)


    return (True, prune)

def single_constraints_FC(constraints):
    single = []

    for c in constraints:
        # check if constraint is unassigned

        if c.get_n_unasgn() == 1:
            # append to single 
            temp_tuple = (c, c.get_unasgn_vars()[0])
            single.append(temp_tuple)


    return single


def prop_GAC(csp, newVar=None):

    constraints = csp.get_all_cons()
    if newVar != None: 
        constraints = csp.get_cons_with_var(newVar)

    # prune values
    prune = []
    while len(constraints) > 0:

        constraint = constraints.pop(0)
        items = constraint.get_scope()

        for i in items:
            for val in i.cur_domain():

                # find values to prune and commence with the pruning
                if constraint.has_support(i, val) == False:
                    prune.append((i, val))
                    i.prune_value(val)
                    if len(i.cur_domain()) == 0:
                        return (False, prune)
                    else:
                        for new in csp.get_cons_with_var(i):
                            if new not in constraints:
                                constraints.append(new)
    return (True, prune)
