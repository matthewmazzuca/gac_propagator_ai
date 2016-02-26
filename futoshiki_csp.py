#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

'''
Construct and return Futoshiki CSP models.
'''

from cspbase import *
import itertools
import copy


def futoshiki_csp_model_1(initial_futoshiki_board):
    '''Return a CSP object representing a Futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, var_arr

    where futoshiki_csp is a csp representing futoshiki using model_1 and
    var_arr is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that var_arr[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))


    The input board is specified as a list of n lists. Each of the n lists
    represents a row of the board. If a 0 is in the list it represents an empty
    cell. Otherwise if a number between 1--n is in the list then this
    represents a pre-set board position.

    Each list is of length 2n-1, with each space on the board being separated
    by the potential inequality constraints. '>' denotes that the previous
    space must be bigger than the next space; '<' denotes that the previous
    space must be smaller than the next; '.' denotes that there is no
    inequality constraint.

    E.g., the board

    -------------------
    | > |2| |9| | |6| |
    | |4| | | |1| | |8|
    | |7| <4|2| | | |3|
    |5| | | | | |3| | |
    | | |1| |6| |5| | |
    | | <3| | | | | |6|
    |1| | | |5|7| |4| |
    |6> | |9| < | |2| |
    | |2| | |8| <1| | |
    -------------------
    would be represented by the list of lists

    [[0,'>',0,'.',2,'.',0,'.',9,'.',0,'.',0,'.',6,'.',0],
     [0,'.',4,'.',0,'.',0,'.',0,'.',1,'.',0,'.',0,'.',8],
     [0,'.',7,'.',0,'<',4,'.',2,'.',0,'.',0,'.',0,'.',3],
     [5,'.',0,'.',0,'.',0,'.',0,'.',0,'.',3,'.',0,'.',0],
     [0,'.',0,'.',1,'.',0,'.',6,'.',0,'.',5,'.',0,'.',0],
     [0,'.',0,'<',3,'.',0,'.',0,'.',0,'.',0,'.',0,'.',6],
     [1,'.',0,'.',0,'.',0,'.',5,'.',7,'.',0,'.',4,'.',0],
     [6,'>',0,'.',0,'.',9,'.',0,'<',0,'.',0,'.',2,'.',0],
     [0,'.',2,'.',0,'.',0,'.',8,'.',0,'<',1,'.',0,'.',0]]


    This routine returns Model_1 which consists of a variable for each cell of
    the board, with domain equal to [1,...,n] if the board has a 0 at that
    position, and domain equal [i] if the board has a fixed number i at that
    cell.

    Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between all relevant
    variables (e.g., all pairs of variables in the same row, etc.).

    All of the constraints of Model_1 MUST BE binary constraints (i.e.,
    constraints whose scope includes two and only two variables).
    '''
    board_dim = len(initial_futoshiki_board) #board_dim := n
    #Construct var_arr

    var_arr = gen_var_arr(board_dim, initial_futoshiki_board)

    #Construct CSP
    futoshiki_csp = make_CSP(var_arr, board_dim)

    #Construct satisfying tuples

    #satisfying tuples for variable pairs (x,y) with no inequality

    wo_ineq = []

    #satisfying tuples for variable pairs (x,y) such that x < y 
    x_less_y = [] 

    #satisfying tuples for variable pairs (x,y) such that x > y
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
    #Add column constraints
    get_col_constraints(board_dim, var_arr, wo_ineq, futoshiki_csp, 1)
    #Done
    return (futoshiki_csp, var_arr)

#IMPLEMENT



def futoshiki_csp_model_2(initial_futoshiki_board):
    '''Return a CSP object representing a futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, var_arr

    where futoshiki_csp is a csp representing futoshiki using model_2 and
    var_arr is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that var_arr[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))

    The input board takes the same input format (a list of n lists of size 2n-1
    specifying the board) as futoshiki_csp_model_1.

    The variables of Model_2 are the same as for Model_1: a variable for each
    cell of the board, with domain equal to [1,...,n] if the board has a 0 at
    that position, and domain equal [n] if the board has a fixed number i at
    that cell.

    However, Model_2 has different constraints. In particular, instead of
    binary non-equals constaints Model_2 has 2*n all-different constraints:
    all-different constraints for the variables in each of the n rows, and n
    columns. Each of these constraints is over n-variables (some of these
    variables will have a single value in their domain). Model_2 should create
    these all-different constraints between the relevant variables, and then
    separately generate the appropriate binary inequality constraints as
    required by the board. There should be j of these constraints, where j is
    the number of inequality symbols found on the board.  
    '''
    board_dim = len(initial_futoshiki_board) #board_dim := n
    #Construct var_arr
    var_arr = []
    for row in range(board_dim):
        column_array = []
        for column in range(board_dim):
            if initial_futoshiki_board[row][column*2] is 0:
                column_array.insert(len(column_array), Variable('{},{}'.format(row, column), range(1,board_dim+1)))
            else:
                column_array.insert(len(column_array), Variable('{},{}'.format(row, column), [initial_futoshiki_board[row][column*2]]))
        var_arr.insert(len(var_arr), copy.deepcopy(column_array))
        
    #Construct CSP
    futoshiki_csp = make_CSP(var_arr, board_dim)

    #satisfying tuples for variable sets (x_1,x_2,...,x_n) with no inequality
    wo_ineq = futoshiki_model_2_tuples(board_dim)

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
#IMPLEMENT


############################## Supplementary 

def make_CSP(var_arr, board_dim):
  futoshiki_csp = CSP('futoshiki[{}]'.format(board_dim))

  for row in range(len(var_arr)): #Add variables to CSP
      for variable in var_arr[row]:
          futoshiki_csp.add_var(variable)

  return futoshiki_csp



def gen_var_arr(board_dim, initial_futoshiki_board):
  var = []

  for row in range(board_dim):
        column_array = []
        for column in range(board_dim):
            if initial_futoshiki_board[row][column*2] is 0:
                column_array.insert(len(column_array), Variable('{},{}'.format(row, column), range(1,board_dim+1)))
            else:
                column_array.insert(len(column_array), Variable('{},{}'.format(row, column), [initial_futoshiki_board[row][column*2]]))
        var.insert(len(var), copy.deepcopy(column_array))

  return var

def get_ineq_contraints(board_dim, var_arr, wo_ineq, initial_futoshiki_board, \
                        futoshiki_csp, x_great_y, x_less_y, model_id):
    if model_id ==1:
        for row in range(board_dim):
            for var1 in range(board_dim):
                for var2 in range(var1 + 1, board_dim):
                    constraint = Constraint('[({},{})({},{})]'.format(row,var1,row,var2), 
                            (var_arr[row][var1], var_arr[row][var2]))
                    if var2 == (var1 + 1) and initial_futoshiki_board[row][var1*2+1] is '>':
                        constraint.add_satisfying_tuples(x_great_y)
                    elif var2 == (var1 + 1) and initial_futoshiki_board[row][var1*2+1] is '<':
                        constraint.add_satisfying_tuples(x_less_y)
                    else:
                        constraint.add_satisfying_tuples(wo_ineq)
                    futoshiki_csp.add_constraint(constraint)
    else:
        for row in range(board_dim):
            for var1 in range(board_dim):
                for var2 in range(var1 + 1, board_dim):
                    constraint = Constraint('[({},{})({},{})]'.format(row,var1,row,var2), 
                            (var_arr[row][var1], var_arr[row][var2]))
                    if var2 == (var1 + 1) and initial_futoshiki_board[row][var1*2+1] is '>':
                        constraint.add_satisfying_tuples(x_great_y)
                        futoshiki_csp.add_constraint(constraint)
                    elif var2 == (var1 + 1) and initial_futoshiki_board[row][var1*2+1] is '<':
                        constraint.add_satisfying_tuples(x_less_y)
                        futoshiki_csp.add_constraint(constraint)


    return futoshiki_csp

def get_col_constraints(board_dim, var_arr, wo_ineq, futoshiki_csp, model_id):
    if model_id == 1:
        for column in range(board_dim):
            for var1 in range(board_dim):
                for var2 in range(var1 + 1, board_dim):
                    constraint = Constraint('[({},{})({},{})]'.format(var1,column,var2,column),
                        (var_arr[var1][column], var_arr[var2][column]))
                    constraint.add_satisfying_tuples(wo_ineq)
                    futoshiki_csp.add_constraint(constraint)
    else:
        for row in range(board_dim):
            variable_scope = []
            for column in range(board_dim):
                variable_scope.append(var_arr[row][column])
            constraint = Constraint('[row {}]'.format(row), tuple(variable_scope))
            constraint.add_satisfying_tuples(wo_ineq)
            futoshiki_csp.add_constraint(constraint)
        #Add column constraints
        for column in range(board_dim):
            variable_scope = []
            for row in range(board_dim):
                variable_scope.append(var_arr[row][column])
            constraint = Constraint('[column {}]'.format(column), tuple(variable_scope))
            constraint.add_satisfying_tuples(wo_ineq)
            futoshiki_csp.add_constraint(constraint)

    return futoshiki_csp

def futoshiki_model_2_tuples(n, tuple_list=None): #Constructs all satisfying tuple combinations of length n
    if tuple_list is None:
        tuple_list = [[1]]
    if len(tuple_list[0]) is n:
        return_list = []
        for item in tuple_list:
            return_list.append(tuple(item))
        return return_list
    else:
        level = len(tuple_list[0]) + 1
        new_list = []
        for item in tuple_list:
            for index in range(0, len(item)+1):
                new_item = copy.deepcopy(item)
                new_item.insert(index, level)
                new_list.append(new_item)
        return futoshiki_model_2_tuples(n, new_list)