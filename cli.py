def yes_or_no(question:str)->bool:
    answer = str()
    while True:
        answer = input(question+'?[y/n]')
        if answer.capitalize().__contains__('Y'):
            return True
        elif answer.capitalize().__contains__('N'):
            return False
        

def print_choices(options:list):
    print('Please reply with:')
    i  = 0
    for option in options:
        i+=1
        print(i,':',option)

def enter_str(min:int=None,max:int=None):
    answer = input()
    if min and len(answer)<min:
        print(f'Please make an entry of at least {min} characters')
        return enter_str(min,max)
    elif min and len(answer)>max:
        print(f'Please make an entry of at most {max} characters')
        return enter_str(min,max)
    return answer

def enter_float(min:float=None,max:float=None)->float:
    try:
        answer = float(enter_str())
        if min and answer<min:
            print('Please enter a value greater than',min)
            return enter_float(min,max)
        elif max and answer>max:
            print('Please enter a value less than',max)
            return enter_float(min,max)
        return answer
    except:
        print('Please enter and number')
        return enter_float(min,max)
    
    
def enter_integer(min:int=None,max:int=None)->int:
    return int(enter_float(min,max))

def choose_one(options:list)->int:
    print_choices(options)
    choice = enter_integer(1,len(options))
    return choice