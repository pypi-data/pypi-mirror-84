import re
def join_space(input="this is for test",sep="__"):
    result = sep.join(re.split(r'\s+',input) )
    return result
def print_input_error():
    print('''
    ================================================================
    enter correct input type  
    ================================================================
    ''')
    print("enter correct input!")
    print("exe ) python -m test.test str__001 sep__001")

if __name__ == "__main__":
    import sys
    argv_n = len(sys.argv)
    if argv_n == 1:
        print_input_error()
    elif argv_n == 2:
        result = join_space(sys.argv[1])
        print(result)
    elif argv_n == 3:
        result = join_space(sys.argv[1],sys.argv[2])
        print(result)
    else :
        print_input_error()
    