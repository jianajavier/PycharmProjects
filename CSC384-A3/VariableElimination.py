from BayesianNetwork import *

##Implement all of the following functions

## Do not modify any of the objects passed in as parameters!
## Create a new Factor object to return when performing factor operations



'''
multiply_factors(factors)

Parameters :
              factors : a list of factors to multiply
Return:
              a new factor that is the product of the factors in "factors"
'''
def multiply_factors(factors):
    product_name = ''
    product_scope = []

    for index, factor in enumerate(factors):
        product_name += factor.name + ' x '
        for variable in factor.get_scope():
            if variable not in product_scope:
                product_scope.append(variable)

    product = Factor(product_name, product_scope)

    for assignment in product.get_assignment_iterator():
        value = 1
        for f in factors:
            ind_list = []
            for var in f.get_scope():
                ind_list.append(product_scope.index(var))
            ass_list = []
            for i in ind_list:
                ass_list.append(assignment[i])
            value *= f.get_value(ass_list)
        product.add_value_at_assignment(value, assignment)

    return product


'''
restrict_factor(factor, variable, value):

Parameters :
              factor : the factor to restrict
              variable : the variable to restrict "factor" on
              value : the value to restrict to
Return:
              A new factor that is the restriction of "factor" by
              "variable"="value"
      
              If "factor" has only one variable its restriction yields a 
              constant factor
'''
def restrict_factor(factor, variable, value):
    name = 'r' + factor.name
    scope = factor.get_scope()
    ind_to_delete = scope.index(variable)
    del scope[ind_to_delete]

    restricted = Factor(name, scope)
    for assgn in factor.get_assignment_iterator():
        if assgn[ind_to_delete] == value:
            val = factor.get_value(assgn)
            del assgn[ind_to_delete]
            restricted.add_value_at_assignment(val, assgn)

    return restricted
    
'''    
sum_out_variable(factor, variable)

Parameters :
              factor : the factor to sum out "variable" on
              variable : the variable to sum out
Return:
              A new factor that is "factor" summed out over "variable"
'''
def sum_out_variable(factor, variable):
    name = 's' + factor.name
    scope = factor.get_scope()
    ind_to_delete = scope.index(variable)
    del scope[ind_to_delete]

    summed_out = Factor(name, scope)

    dom = variable.domain()

    for assgn in summed_out.get_assignment_iterator():
        summed = 0
        for v in dom:
            find_value = list(assgn)
            find_value.insert(ind_to_delete, v)
            summed += factor.get_value(find_value)
        summed_out.add_value_at_assignment(summed, assgn)

    if len(factor.get_scope()) == 1:
        if factor.get_scope()[0] == variable:
            summed = 0
            for value in variable.domain():
                summed += factor.get_value([value])
            summed_out.add_value_at_assignment(summed, [])

    return summed_out


    
'''
VariableElimination(net, queryVar, evidenceVars)

 Parameters :
              net: a BayesianNetwork object
              queryVar: a Variable object
                        (the variable whose distribution we want to compute)
              evidenceVars: a list of Variable objects.
                            Each of these variables should have evidence set
                            to a particular value from its domain using
                            the set_evidence function. 

 Return:
         A distribution over the values of QueryVar
 Format:  A list of numbers, one for each value in QueryVar's Domain
         -The distribution should be normalized.
         -The i'th number is the probability that QueryVar is equal to its
          i'th value given the setting of the evidence
 Example:

 QueryVar = A with Dom[A] = ['a', 'b', 'c'], EvidenceVars = [B, C]
 prior function calls: B.set_evidence(1) and C.set_evidence('c')

 VE returns:  a list of three numbers. E.g. [0.5, 0.24, 0.26]

 These numbers would mean that Pr(A='a'|B=1, C='c') = 0.5
                               Pr(A='b'|B=1, C='c') = 0.24
                               Pr(A='c'|B=1, C='c') = 0.26
'''       
def VariableElimination(net, queryVar, evidenceVars):
    factors = net.factors()
    factors_copy = []
    z = []

    for f in factors:
        replaced = False
        for e in evidenceVars:
            if e in f.get_scope():

                replace = restrict_factor(f, e, e.get_evidence())
                for evid in evidenceVars:
                    if evid in replace.get_scope():
                        replace = restrict_factor(replace, evid, evid.get_evidence())
                replaced = True
                factors_copy.append(replace)

        for v in f.get_scope():
            if v not in evidenceVars and v not in z and v != queryVar:
                z.append(v)
        if replaced == False:
            factors_copy.append(f)

    z = min_fill_ordering(factors_copy, queryVar)

    for zi in z:
        include_zi = []
        for f in factors_copy:
            if zi in f.get_scope():
                include_zi.append(f)
        new_factor = sum_out_variable(multiply_factors(include_zi), zi)
        for zi_in in include_zi:
            ind = factors_copy.index(zi_in)
            del factors_copy[ind]
        factors_copy.append(new_factor)

    remaining = multiply_factors(factors_copy)
    alpha = sum_out_variable(remaining, queryVar)

    probability = []
    for assign in remaining.get_assignment_iterator():
        to_add = remaining.get_value(assign)
        probability.append(to_add/alpha.get_value([]))

    return probability

