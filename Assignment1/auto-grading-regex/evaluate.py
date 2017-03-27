import data_reader as dr
import sys
import regex_validate as rv
import json

# Read configuration.
with open("grading_config.json") as jc_file: grading_config = json.load(jc_file)
total_marks_key = "total_marks"
marks_division_key = "marks_division"


def calculate_marks(prblm, total_tests, total_mistakes, should_print):
    try:
        total_marks_of_prblm = (grading_config[total_marks_key]*grading_config[marks_division_key][prblm])*1.0
    except KeyError:
        print_output("Scoring criteria for {0} is not provided in the config".format(prblm), should_print)
        return 0
    marks_per_test_case = total_marks_of_prblm/total_tests
    deductions = total_mistakes*marks_per_test_case
    marks_scored = total_marks_of_prblm - deductions
    return marks_scored


def evaluate_problem(test_cases, prblm, sol, should_print):
    marks_scored = 0
    try:  # Valid problem.
        marks_scored = grade_problem(test_cases, prblm, sol, should_print)
    except KeyError:
        print_output("Invalid problem {0}".format(prblm), should_print)
    print_output("---------------------------------------------------------------------------", should_print)
    return marks_scored


def grade_problem(test_cases, prblm, sol, should_print):
    test_case = test_cases[prblm]
    print_output("Evaluating {0}".format(prblm), should_print)
    false_neg, false_pos = rv.validate(sol, test_case[0], test_case[1], test_case[2])
    if len(false_neg) == 0 and len(false_pos) == 0:
        print_output("{0} passed".format(prblm), should_print)
    else:
        report_false_negatives(false_neg, should_print)
        report_false_positives(false_pos, should_print)
    marks_scored = calculate_marks(prblm, len(test_case[0]) + len(test_case[1]),
                                   len(false_neg) + len(false_pos), should_print)
    marks_scored = round(marks_scored, 2)
    print_output("Score: {0:.2f}".format(marks_scored), should_print)
    return marks_scored


def report_false_negatives(false_neg, should_print):
    if len(false_neg) > 0:
        print_output("Following expressions should have been matched by your regex but didn't match.", should_print)
        for expr in false_neg:
            print_output("\t {0}".format(expr), should_print)


def report_false_positives(false_pos, should_print):
    if len(false_pos) > 0:
        print_output("Following expressions should not have been matched by your regex but did match.", should_print)
        for expr in false_pos:
            print_output("\t {0}".format(expr), should_print)


def evaluate(sol_file, should_print):
    prblm_wise_score = {}
    # Read solutions
    solutions = dr.read_solution(sol_file)
    # Read test cases.
    test_cases = dr.read_test_cases()
    print_output("Starting evaluation of regex. For each regex, we will show false positive matches and false negative matches, if any."
                  , should_print)
    total_score = 0
    # Evaluate for each problem
    for prblm, sol in sorted(solutions.iteritems()):
        prblm_score = evaluate_problem(test_cases, prblm, sol, should_print)
        total_score += prblm_score
        prblm_wise_score[prblm] = prblm_score
    print_output("Total Score: {0:.2f}/{1}".format(round(total_score, 2), grading_config[total_marks_key]), should_print)
    return prblm_wise_score, total_score


def problem_names():
    return sorted(dr.read_test_cases().keys())

def print_output(message, should_print):
    if should_print:
        print message


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Solution file should be provided as first command line argument."
        sys.exit(0)
    sol_file = sys.argv[1]
    evaluate(sol_file, True)
