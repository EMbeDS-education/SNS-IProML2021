#These two functions replace 'input()'
def my_read_list(lst_param):
    for i in lst_param:
        yield i

def my_input(*args, **kwargs):
    return next(_inputs_provider)


#Store the original function for 'input()'
from ipykernel.ipkernel import IPythonKernel
ipython_input = IPythonKernel._input_request


#Store the original function for 'print()'
import sys
ipython_output = sys.stdout


#Library to print information on exceptions
import traceback


#Test each line from expected/actual output
def test_outputs(file_out,expected_output):
    with open(file_out) as f:
        actual_output = f.readlines()
    lines_to_compare=min(len(actual_output),len(expected_output))
    if len(actual_output)!=len(expected_output):
        print(' Test FAILED!')
        print('  The program should print',len(expected_output),'lines while there are',len(actual_output))
        print('  Nevetheless, we compare the first',lines_to_compare,'lines')
        print()
    else:
        print('  The program prints',len(expected_output),'lines as expected.')
    for i in range(lines_to_compare):
        print(' Line',i)
        assert_equals(actual_output[i],expected_output[i])

def assert_equals(actual,expected,failure_message=""):
    if actual != None and type(actual)==str:
        actual=actual.strip()
    if expected != None and type(expected)==str:        
        expected=expected.strip()
    if(expected==actual):
        #print('Test passed')
        print('  Expected and actual output match:',expected)
    else:
        print('  Test FAILED')
        print('    Expected:',expected)
        print('    Actual:',actual)
        if(failure_message!=""):
            print(failure_message)
    print()  
    
    
#Run the assignment of the student, and test its output
def run_and_test(inputs,expected_outputs,asgn,title="",file_out="stdout.txt"):
    global _inputs_provider
    exception_generated=False
    if len(title)==0:
        title=str(inputs)
    try:
        try:
            #Replace input() with my_input()
            IPythonKernel._input_request = my_input
            _inputs_provider=my_read_list(inputs)

            #Write in a file rather than in the terminal
            sys.stdout = open(file_out, 'w')

            #Run the code of the student
            asgn()

        finally:
            #Restore the correct input() and print()
            IPythonKernel._input_request = ipython_input
            sys.stdout = ipython_output
            print('Test',title)
    except StopIteration as err:
            exception_generated=True
            print(' You are making too many `input()`. Please check your code.')
            print(' The problem arised executing the following command:')
            #raise err
            traceback.print_exc(limit=2)

    if not(exception_generated):
        #assert_equals("abc","abc")
        #assert_equals("abc","abcd")
        test_outputs(file_out,expected_outputs)