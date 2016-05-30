#Implement the function DecisionSupport

'''
For this question you may use the code from part 1

Note however that part 2 will be marked independent of part 1

The solution for VariableElimination.py will be used for testing part2 instead
of the copy you submit. 
'''

from MedicalBayesianNetwork import *
from VariableElimination import *

'''
Parameters:
             medicalNet - A MedicalBayesianNetwork object                        

             patient    - A Patient object
                          The patient to calculate treatment-outcome
                          probabilites for
Return:
         -A factor object

         This factor should be a probability table relating all possible
         Treatments to all possible outcomes
'''
def DecisionSupport(medicalNet, patient):
    bayes = medicalNet.net

    treatment_vars = medicalNet.getTreatmentVars()
    outcome_vars = medicalNet.getOutcomeVars()
    patient_evidence = patient.evidenceVariables()
    medicalNet_factors = bayes.factors()

    medicalNet.set_evidence_by_patient(patient)

    prob_table = Factor('Probability Table', [x for x in treatment_vars] + [x for x in outcome_vars])
    treatment_factor = Factor('Treatment Factors', treatment_vars)

    # iterate over different fixed treatments
    for assgn in treatment_factor.get_assignment_iterator():
        for index in range(len(treatment_factor.get_scope())):
            treatment_factor.get_scope()[index].set_evidence(assgn[index])

        remaining = VariableElimination2(outcome_vars, [x for x in treatment_vars] + [x for x in patient_evidence],
                                         medicalNet_factors)

        for assgn1 in remaining.get_assignment_iterator():
            prob_table.add_value_at_assignment(remaining.get_value(assgn1), [x for x in assgn] + [x for x in assgn1])

    return prob_table

def VariableElimination2(queryVars, evidenceVars, relevant_factors):
    factor_list = []
    z = []
    for f in relevant_factors:
        replaced = False
        for e in evidenceVars:
            if e in f.get_scope():
                replace = restrict_factor(f, e, e.get_evidence())
                for evidence in evidenceVars:
                    if evidence in replace.get_scope():
                        replace = restrict_factor(replace, evidence, evidence.get_evidence())
                replaced = True
                factor_list.append(replace)

        for v in f.get_scope():
            if v not in evidenceVars and v not in z and v not in queryVars:
                z.append(v)
        if replaced == False:
            factor_list.append(f)

    for zi in z:
        include_zi = []
        for f in factor_list:
            if zi in f.get_scope():
                include_zi.append(f)
        new_factor = sum_out_variable(multiply_factors(include_zi), zi)
        for zi_in in include_zi:
            ind = factor_list.index(zi_in)
            del factor_list[ind]
        factor_list.append(new_factor)

    if len(factor_list) > 1:
        new_factor = multiply_factors(factor_list)
    else:
        new_factor = factor_list[0]

    final_factor = Factor(new_factor.name, new_factor.get_scope())
    normalize_value = 0
    for assignment in new_factor.get_assignment_iterator():
        normalize_value += new_factor.get_value(assignment)

    for assignment in new_factor.get_assignment_iterator():
        final_factor.add_value_at_assignment(new_factor.get_value(assignment)/normalize_value, assignment)

    return final_factor
