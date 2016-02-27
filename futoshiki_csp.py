from cspbase import *
import itertools
import copy


def futoshiki_csp_model_1(initial_futoshiki_board):

    board_dim = len(initial_futoshiki_board) #board_dim := n
    #Construct var_arr
    var_arr = gen_var_arr(board_dim, initial_futoshiki_board)
    #Construct CSP
    futoshiki_csp = make_CSP(var_arr, board_dim)
    #Construct satisfying tuples
    #satisfying tuples for variable pairs (x,y) with no inequality
    #satisfying tuples for variable pairs (x,y) such that x < y 
    wo_ineq = []
    x_less_y = [] 
    x_great_y = [] 
    for x in range(1, board_dim + 1):
        for y in range(1, board_dim + 1):
            if x != y:
                wo_ineq.append((x,y))
            if x < y:
                x_less_y.append((x,y))
            if x > y:
                x_great_y.append((x,y))

    #Add inequality row constraints
    get_ineq_contraints(board_dim, var_arr, wo_ineq, initial_futoshiki_board, \
                        futoshiki_csp, x_great_y, x_less_y, 1)
    #Add col constraints
    get_col_constraints(board_dim, var_arr, wo_ineq, futoshiki_csp, 1)
    #Done
    return (futoshiki_csp, var_arr)



def futoshiki_csp_model_2(initial_futoshiki_board):
    board_dim = len(initial_futoshiki_board) #board_dim := n
    #Construct var_arr
    var_arr = []
    for item in range(board_dim):
        cols = []
        for col in range(board_dim):
            if initial_futoshiki_board[item][col*2] is 0:
                cols.insert(len(cols), Variable('{},{}'.format(item, col), range(1,board_dim+1)))
            else:
                cols.insert(len(cols), Variable('{},{}'.format(item, col), \
                    [initial_futoshiki_board[item][col*2]]))
        var_arr.insert(len(var_arr), copy.deepcopy(cols))

    #Construct CSP
    futoshiki_csp = make_CSP(var_arr, board_dim)

    #satisfying tuples for variable sets (x_1,x_2,...,x_n) with no inequality
    wo_ineq = gen_tups(board_dim)

    #satisfying tuples for variable pairs (x,y) such that x < y 
    x_less_y = []

    #satisfying tuples for variable pairs (x,y) such that x > y 
    x_great_y = []
    for x in range(1, board_dim + 1):
        for y in range(x, board_dim + 1):
            if x < y:
                x_less_y.append((x,y))
                x_great_y.append((y,x))
    #Add inequality constraints
    get_ineq_contraints(board_dim, var_arr, wo_ineq, initial_futoshiki_board, \
                        futoshiki_csp, x_great_y, x_less_y, 2)
    #Add row constraints
    
    get_col_constraints(board_dim, var_arr, wo_ineq, futoshiki_csp, 2)
    #Done
    return (futoshiki_csp, var_arr)


#########################################################################
##############################Supplementary##############################  
#########################################################################

def make_CSP(var_arr, board_dim):
  futoshiki_csp = CSP('futoshiki[{}]'.format(board_dim))

  for item in range(len(var_arr)): #Add variables to CSP
      for variable in var_arr[item]:
          futoshiki_csp.add_var(variable)

  return futoshiki_csp



def gen_var_arr(board_dim, initial_futoshiki_board):
  var = []

  for item in range(board_dim):
        cols = []
        for col in range(board_dim):
            if initial_futoshiki_board[item][col*2] == 0:
                cols.insert(len(cols), Variable('{},{}'.format(item, col), range(1,board_dim+1)))
            else:
                cols.insert(len(cols), Variable('{},{}'.format(item, col), \
                    [initial_futoshiki_board[item][col*2]]))
        var.insert(len(var), copy.deepcopy(cols))

  return var

def get_ineq_contraints(board_dim, var_arr, wo_ineq, initial_futoshiki_board, \
                        futoshiki_csp, x_great_y, x_less_y, model_id):

    for item in range(board_dim):
        for attr_1 in range(board_dim):
            for attr_2 in range(attr_1 + 1, board_dim):
                if model_id == 1:
                    constraint = Constraint('[({},{})({},{})]'.format(item,attr_1,item,attr_2), 
                            (var_arr[item][attr_1], var_arr[item][attr_2]))
                    if attr_2 == (attr_1 + 1) and initial_futoshiki_board[item][(attr_1*2)+1] == '>':
                        constraint.add_satisfying_tuples(x_great_y)
                    elif attr_2 == (attr_1 + 1) and initial_futoshiki_board[item][(attr_1*2)+1] == '<':
                        constraint.add_satisfying_tuples(x_less_y)
                    else:
                        constraint.add_satisfying_tuples(wo_ineq)
                    futoshiki_csp.add_constraint(constraint)
                else:
                    constraint = Constraint('[({},{})({},{})]'.format(item,attr_1,item,attr_2), 
                            (var_arr[item][attr_1], var_arr[item][attr_2]))
                    if attr_2 == (attr_1 + 1) and initial_futoshiki_board[item][(attr_1*2)+1] == '>':
                        constraint.add_satisfying_tuples(x_great_y)
                        futoshiki_csp.add_constraint(constraint)
                    elif attr_2 == (attr_1 + 1) and initial_futoshiki_board[item][(attr_1*2)+1] == '<':
                        constraint.add_satisfying_tuples(x_less_y)
                        futoshiki_csp.add_constraint(constraint)


    return futoshiki_csp

def get_col_constraints(board_dim, var_arr, wo_ineq, futoshiki_csp, model_id):
    if model_id == 1:
        for col in range(board_dim):
            for attr_1 in range(board_dim):
                for attr_2 in range(attr_1 + 1, board_dim):
                    constraint = Constraint('[({},{})({},{})]'.format(attr_1,col,attr_2,col),
                        (var_arr[attr_1][col], var_arr[attr_2][col]))
                    constraint.add_satisfying_tuples(wo_ineq)
                    futoshiki_csp.add_constraint(constraint)
    else:
        for item in range(board_dim):
            var_scp = []
            for col in range(board_dim):
                var_scp.append(var_arr[item][col])
            constraint = Constraint('[item {}]'.format(item), tuple(var_scp))
            constraint.add_satisfying_tuples(wo_ineq)
            futoshiki_csp.add_constraint(constraint)
        #Add col constraints
        for col in range(board_dim):
            var_scp = []
            for item in range(board_dim):
                var_scp.append(var_arr[item][col])
            constraint = Constraint('[col {}]'.format(col), tuple(var_scp))
            constraint.add_satisfying_tuples(wo_ineq)
            futoshiki_csp.add_constraint(constraint)

    return futoshiki_csp

def gen_tups(n, tuple_list=[[1]]): #Constructs all satisfying tuple combinations of length n
    if len(tuple_list[0]) != n:
        level = len(tuple_list[0]) + 1
        temp = []
        for item in tuple_list:
            for var in range(0, (len(item)+1)):
                new = copy.deepcopy(item)
                new.insert(var, level)
                temp.append(new)
        return gen_tups(n, temp)
    else:
        return_list = []
        for item in tuple_list:
            return_list.append(tuple(item))
        return return_list

        