#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

'''
Construct and return Futoshiki CSP models.
'''

from cspbase import *
import itertools

def futoshiki_csp_model_1(initial_futoshiki_board):
    '''Return a CSP object representing a Futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_1 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
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

#IMPLEMENT

##############################

    size = len(initial_futoshiki_board)
    board = [[0 for x in range(size)] for x in range(size)]
    cons = []
    cons_count = 0

    for idx, row in enumerate(initial_futoshiki_board):
        for idx2, item in enumerate(row[::2]):
            if item == 0:
                board[idx][idx2] = Variable("V({},{})".format(idx,idx2), [(x + 1) for x in list(range(size))])
            else:
                board[idx][idx2] = Variable("V({},{})".format(idx,idx2), [item])
        for idx2, item in enumerate(row[1::2]):
            if item != '.':
                cons.append(Constraint("C({})".format(cons_count), [board[idx][idx2], board[idx][idx2+1]]))
                cons[cons_count].add_satisfying_tuples(generate_satisfying_tuples(item, [board[idx][idx2], board[idx][idx2+1]]))
                cons_count += 1
    vars = []
    for i in range(size):
        for j in range(size):
            vars.append(board[i][j])


    for i in range(size):
        for j in range(size):
            for h in range(j+1, size):
                cons.append(Constraint("C({})".format(cons_count), [board[i][j], board[i][h]]))
                cons[cons_count].add_satisfying_tuples(generate_satisfying_tuples(None, [board[i][j], board[i][h]]))
                cons_count += 1

    for i in range(size):
        for j in range(size):
            for h in range(j+1, size):
                cons.append(Constraint("C({})".format(cons_count), [board[j][i], board[h][i]]))
                cons[cons_count].add_satisfying_tuples(generate_satisfying_tuples(None, [board[j][i], board[h][i]]))
                cons_count += 1


    csp_model_1 = CSP("Futoshiki-M1", vars)
    [csp_model_1.add_constraint(x) for x in cons]

    return csp_model_1, board


def generate_satisfying_tuples(op, var_list):
    # Return list of satisfying tuples
    varDoms = []

    for var in var_list:
        varDoms.append(var.domain())

    sat_tuples = []
    for t in itertools.product(*varDoms):
        if op == '<':
            if lt(t):
                sat_tuples.append(t)
        elif op == '>':
            if gt(t):
                sat_tuples.append(t)
        elif op == 'all-diff':
            if all_diff(t):
                sat_tuples.append(t)
        else:
            if ne(t):
                sat_tuples.append(t)

    return sat_tuples

def gt(v):
    return (v[0] > v[1])

def lt(v):
    return (v[0] < v[1])

def ne(v):
    return v[0] != v[1]

def all_diff(v):
    return len(v) == len(set(v))



def futoshiki_csp_model_2(initial_futoshiki_board):
    '''Return a CSP object representing a futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_2 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
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

#IMPLEMENT

    size = len(initial_futoshiki_board)
    board = [[0 for x in range(size)] for x in range(size)]
    cons = []
    cons_count = 0

    for idx, row in enumerate(initial_futoshiki_board):
        for idx2, item in enumerate(row[::2]):
            if item == 0:
                board[idx][idx2] = Variable("V({},{})".format(idx,idx2), [(x + 1) for x in list(range(size))])
            else:
                board[idx][idx2] = Variable("V({},{})".format(idx,idx2), [item])
        for idx2, item in enumerate(row[1::2]):
            if item != '.':
                cons.append(Constraint("C({})".format(cons_count), [board[idx][idx2], board[idx][idx2+1]]))
                cons[cons_count].add_satisfying_tuples(generate_satisfying_tuples(item, [board[idx][idx2], board[idx][idx2+1]]))
                cons_count += 1
    vars = []
    for i in range(size):
        for j in range(size):
            vars.append(board[i][j])


    for i in range(size):
        cons.append(Constraint("C({})".format(cons_count), board[i][0:size]))
        cons[cons_count].add_satisfying_tuples(generate_satisfying_tuples('all-diff', board[i][0:size]))
        cons_count += 1

    n_ary = []
    for i in range(size):
        sublist = []
        for j in range(size):
            sublist.append(board[j][i])
        n_ary.append(sublist)

    for sub in n_ary:
        cons.append(Constraint("C({})".format(cons_count), sub))
        cons[cons_count].add_satisfying_tuples(generate_satisfying_tuples('all-diff', sub))
        cons_count += 1


    csp_model_2 = CSP("Futoshiki-M2", vars)
    [csp_model_2.add_constraint(x) for x in cons]

    return csp_model_2, board

