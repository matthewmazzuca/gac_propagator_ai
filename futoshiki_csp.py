from cspbase import *
import copy
import itertools



def futoshiki_csp_model_1(initial_futoshiki_board):

    # Get booard dimensions
    board_dim = len(initial_futoshiki_board) 
    #construct array from initial board
    var_arr = gen_var_arr(board_dim, initial_futoshiki_board)
    #make futoshiki csp 
    futoshiki_csp = make_CSP(var_arr, board_dim)

    #Construct list of types
    # set up lists for without inequality, one<y, one>y respectively.  Satisfying
    # tuples will be put in these lists
    wo_ineq = []
    one_less_two = [] 
    one_great_two = [] 
    # append appropriate tuples to list
    # non equal constraints
    for one in range(1, board_dim + 1):
        for two in range(1, board_dim + 1):
            # if first is not second
            if one != two:
                wo_ineq.append((one,two))
            # if first is less than second
            if one < two:
                one_less_two.append((one,two))
            # if first is greater than second
            if one > two:
                one_great_two.append((one,two))

    #get inequality-in-row constraints
    get_ineq_contraints(board_dim, var_arr, wo_ineq, initial_futoshiki_board, \
                        futoshiki_csp, one_great_two, one_less_two, 1)
    #get column constraints
    get_col_constraints(board_dim, var_arr, wo_ineq, futoshiki_csp, 1)

    return (futoshiki_csp, var_arr)



def futoshiki_csp_model_2(initial_futoshiki_board):
    
    # get board dimensions
    board_dim = len(initial_futoshiki_board)
    #Construct var_arr
    var_arr = gen_var_arr(board_dim, initial_futoshiki_board)
    

    #Construct CSP
    futoshiki_csp = make_CSP(var_arr, board_dim)

    #satisfying tuples for variable sets (one_1,one_2,...,one_n) with no inequality
    wo_ineq = gen_tups(board_dim)

    #satisfying tuples for variable pairs (one,y) such that one < y 
    one_less_two = []

    #satisfying tuples for variable pairs (one,y) such that one > y 
    one_great_two = []
    for one in range(1, board_dim + 1):
        for two in range(one, board_dim + 1):
            # append tuples to lists
            # set up for all constraints
            if one < two:
                # if first is less than second append both in reverse order
                one_less_two.append((one,two))
                one_great_two.append((two,one))
    #Add inequality constraints
    get_ineq_contraints(board_dim, var_arr, wo_ineq, initial_futoshiki_board, \
                        futoshiki_csp, one_great_two, one_less_two, 2)
    #Add row constraints
    
    get_col_constraints(board_dim, var_arr, wo_ineq, futoshiki_csp, 2)
    #Done
    return (futoshiki_csp, var_arr)


#########################################################################
##############################Supplementary##############################  
#########################################################################

def make_CSP(var_arr, board_dim):
    # construct fukoshiki csp

    futoshiki_csp = CSP('futoshiki[{}]'.format(board_dim))

    for item in range(len(var_arr)): 
    #add each variable to csp
        for variable in var_arr[item]:
          futoshiki_csp.add_var(variable)

    # return csp construct
    return futoshiki_csp



def gen_var_arr(board_dim, initial_futoshiki_board):

    # generate variable array from the initial board
    var = []

    for item in range(board_dim):
        # get columns in the board and collect variables into an array
        cols = []
        for col in range(board_dim):
            if initial_futoshiki_board[item][col*2] == 0:
                cols.insert(len(cols), Variable('{},{}'.format(item, col), range(1,board_dim+1)))
            else:
                cols.insert(len(cols), Variable('{},{}'.format(item, col), \
                    [initial_futoshiki_board[item][col*2]]))
        # make copy for completeness
        var.insert(len(var), copy.deepcopy(cols))

    return var

def get_ineq_contraints(board_dim, var_arr, wo_ineq, initial_futoshiki_board, \
                        futoshiki_csp, one_great_y, one_less_y, model_id):
    # get inequality constraints
    # function for both models
    # formatting done as per model_id

    for item in range(board_dim):
        for attr_1 in range(board_dim):
            for attr_2 in range(attr_1 + 1, board_dim):
                # get row, collumn attributes in board
                # get up attr1 up until the end of board
                if model_id == 1:
                    # if model one  only binary not equal constraints for the row and column
                    # constraints, and binary inequality constraints.

                    # initialize contraint
                    constraint = Constraint('[({},{})({},{})]'.format(item,attr_1,item,attr_2), 
                            (var_arr[item][attr_1], var_arr[item][attr_2]))
                    # cjcelc of greater
                    if attr_2 == (attr_1 + 1) and initial_futoshiki_board[item][(attr_1*2)+1] == '>':
                        constraint.add_satisfying_tuples(one_great_y)
                    # check if less than
                    elif attr_2 == (attr_1 + 1) and initial_futoshiki_board[item][(attr_1*2)+1] == '<':
                        constraint.add_satisfying_tuples(one_less_y)
                    else:
                        # else there is no inequality
                        constraint.add_satisfying_tuples(wo_ineq)
                    futoshiki_csp.add_constraint(constraint)
                else:
                    # if model two all-different constraints for the row and column constraints,
                    # and binary inequality constraints.

                    # initialize constraint
                    constraint = Constraint('[({},{})({},{})]'.format(item,attr_1,item,attr_2), 
                            (var_arr[item][attr_1], var_arr[item][attr_2]))
                    # check if greater than
                    if attr_2 == (attr_1 + 1) and initial_futoshiki_board[item][(attr_1*2)+1] == '>':
                        constraint.add_satisfying_tuples(one_great_y)
                        futoshiki_csp.add_constraint(constraint)
                    # check if less than
                    elif attr_2 == (attr_1 + 1) and initial_futoshiki_board[item][(attr_1*2)+1] == '<':
                        constraint.add_satisfying_tuples(one_less_y)
                        futoshiki_csp.add_constraint(constraint)

    return futoshiki_csp

def get_col_constraints(board_dim, var_arr, wo_ineq, futoshiki_csp, model_id):
    # get column contraints for both models

    # if model id is one we need satisfying items without inequalities, 
    # so we need to find these contraints
    if model_id != 1:
        for item in range(board_dim):
            # initialize the variable scope

            var_scp = []
            for col in range(board_dim):
                var_scp.append(var_arr[item][col])
            # get no inequality tuples and add satisfying tuples
            constraint = Constraint('[item {}]'.format(item), tuple(var_scp))
            constraint.add_satisfying_tuples(wo_ineq)
            futoshiki_csp.add_constraint(constraint)

    for col in range(board_dim):
        # now we need to get  column constraints
        if model_id == 1:
            for attr_1 in range(board_dim):
                for attr_2 in range(attr_1 + 1, board_dim):
                    constraint = Constraint('[({},{})({},{})]'.format(attr_1,col,attr_2,col),
                        (var_arr[attr_1][col], var_arr[attr_2][col]))
                    constraint.add_satisfying_tuples(wo_ineq)
                    futoshiki_csp.add_constraint(constraint)
        else:
            var_scp = []
            for item in range(board_dim):
                var_scp.append(var_arr[item][col])
            constraint = Constraint('[col {}]'.format(col), tuple(var_scp))
            constraint.add_satisfying_tuples(wo_ineq)
            futoshiki_csp.add_constraint(constraint)

    return futoshiki_csp

def gen_tups(n, tups=[[1]]): 
    #generate all tuples of length n
    if len(tups[0]) != n:
        # get level
        attr = len(tups[0]) + 1
        temp = []
        for item in tups:
            for var in range(0, (len(item)+1)):
                new = copy.deepcopy(item)
                new.insert(var, attr)
                temp.append(new)
        return gen_tups(n, temp)
    else:
        return_list = []
        for item in tups:
            return_list.append(tuple(item))
        return return_list

        