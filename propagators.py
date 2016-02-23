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
import copy

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
    '''Do forward checking.  That is, check constraints with only one
    uninstantiated variable, and prune appropriately.  (i.e., do not prune a
    value that has already been pruned; do not prune the same value twice.)
    Return if a deadend has been detected, and return the variable/value pairs
    that have been pruned.  See beginning of this file for complete description
    of what propagator functions should take as input and return.

    Input: csp, (optional) newVar.
        csp is a CSP object---the propagator uses this to
        access the variables and constraints.

        newVar is an optional argument.
        if newVar is not None:
            then newVar is the most recently assigned variable of the search.
            run FC on all constraints that contain newVar.
        else:
            propagator is called before any assignments are made in which case
            it must decide what processing to do prior to any variable
            assignment.

    Returns: (boolean,list) tuple, where list is a list of tuples:
             (True/False, [(Variable, Value), (Variable, Value), ... ])

        boolean is False if a deadend has been detected, and True otherwise.

        list is a set of variable/value pairs that are all of the values the
        propagator pruned.
    '''

#IMPLEMENT
    if newVar == None:
        constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)

    # print contraints #for testing

    single = []
    for c in constraints:
        if c.get_n_unasgn() == 1:
            temp_tuple = (c, c.get_unasgn_vars()[0])
            single.append(temp_tuple)

    # print("Single", single)

    # sorted_constraints = sorted(single, key=get_key)
    if single == []:
        print("single", '[]')
    else:
        for s in single:
            print("single", s)
    #Conduct forward checking


    prune_vals = []
    while len(single) > 0:
        constraint,unasgn_var = single.pop()
        cur_dom = copy.deepcopy(unasgn_var.cur_domain())
        for val in cur_dom:
            testing_values = []
            for var in constraint.get_scope():
                if var is not unasgn_var:
                    testing_values.append(var.get_assigned_value())
                else:
                    testing_values.append(val)
            if not constraint.check(testing_values):
                prune_vals.append((unasgn_var, val))
                unasgn_var.prune_value(val)
                if len(unasgn_var.cur_domain()) is 0: #reached DWO
                    return (False, prune_vals)


    return (True, prune_vals)

def get_key(item):
    return len(item[1].cur_domain())


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation, as described in lecture. See beginning of this file
    for complete description of what propagator functions should take as input
    and return.

    Input: csp, (optional) newVar.
        csp is a CSP object---the propagator uses this to access the variables
        and constraints.

        newVar is an optional argument.
        if newVar is not None:
            do GAC enforce with constraints containing newVar on the GAC queue.
        else:
            Do initial GAC enforce, processing all constraints.

    Returns: (boolean,list) tuple, where list is a list of tuples:
             (True/False, [(Variable, Value), (Variable, Value), ... ])

    boolean is False if a deadend has been detected, and True otherwise.

    list is a set of variable/value pairs that are all of the values the
    propagator pruned.
    '''

#IMPLEMENT

    check_constraints = []
    if newVar is None: #Check all constraints
        check_constraints = csp.get_all_cons()
    else: #Check only constraints containing newVar
        check_constraints = csp.get_cons_with_var(newVar)
    #Check if variables have support for each value
    prune_vals = []
    while len(check_constraints) > 0:
        constraint = check_constraints.pop(0)
        variables = constraint.get_scope()
        for variable in variables:
            for value in variable.cur_domain():
                if constraint.has_support(variable, value) is False:
                    prune_vals.append((variable, value))
                    variable.prune_value(value)
                    if len(variable.cur_domain()) is 0: #reached DWO
                        return (False, prune_vals)
                    else:
                        for new_constraint in csp.get_cons_with_var(variable):
                            if new_constraint not in check_constraints:
                                check_constraints.append(new_constraint)
    return (True, prune_vals)
