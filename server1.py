from base import UnitScores
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import xmlrpc.client as client

person_id = None
GRADE_A = 80
GRADE_B = 70
GRADE_C = 60
GRADE_D = 50
GRADE_E = 40

def display_unit_scores(unit_scores:UnitScores):
    print('| Unit \t\t| Score\t|')
    print('-------------------------')
    for unit, score in unit_scores:
        print(f'| {unit}  \t| {score}\t|')

    print('-------------------------')

def grading(unit_scores):
    graded_unit_scores=[]
    for unit, score in unit_scores:
        grade = None
        if score>=GRADE_A:
            grade='A'
        elif score>=GRADE_B:
            grade='B'
        elif score>=GRADE_C:
            grade='C'
        elif score>=GRADE_D:
            grade='D'
        elif score>=GRADE_E:
            grade='E'
        elif score<GRADE_E:
            grade='F'
        graded_unit_scores.append((unit,score,grade))

    return graded_unit_scores


def get_course_average(unit_scores:UnitScores)->float:
    total = sum([score for _, score in unit_scores])
    return total/len(unit_scores)

def get_best_8(unit_scores:UnitScores)->list:
    if len(unit_scores)<=8:
        return unit_scores
    else:
        scores = [x for _ , x in unit_scores]
        best_8 = []
        for i in range(8):
            best_score  = max(scores)
            best_8.append(best_score)
            scores.remove(best_score)
        return best_8

def best_average(unit_scores:UnitScores)->float:
    return sum(get_best_8(unit_scores))/8
class EvaluationPipeline:
    """
    Connects the series of evaluation steps required
    """
    def __init__(self,unit_scores,person_id) -> None:
        self.unit_scores = unit_scores
        self.person_id = person_id
        self.course_average = get_course_average(self.unit_scores)
        self.best_average = best_average(unit_scores)
        self.disqualify = 'DOES NOT QUALIFY FOR HONORS STUDY'
        self.qualify = 'QUALIFIES FOR HONOURS STUDY'

    def evaluate(self):
        """
        Starts the evaluation process
        """
        return self.step1()
    def step1(self):
        if len(self.unit_scores)<16:
            return f'id={self.person_id}, course_average={self.course_average}, completed less than 16 units!\n {self.disqualify}'
        return self.step2()
        
    def step2(self):
        graded_unit_scores = grading(self.unit_scores)
        grades = [grade for _,_,grade in graded_unit_scores]
        fails = grades.count('F')
        if fails>=6:
            return f'id={self.person_id}, course_average={self.course_average}, with 6 or more Fails! {self.disqualify}'
        return self.step3()
    
    def step3(self):
        if self.course_average>=70:
            return f'id={self.person_id}, course_average={self.course_average}, {self.qualify}'
        return self.step4()
    
    def step4(self):
        if self.course_average >= 65 and self.course_average<=70 and self.best_average>=80:
            return f'id={self.person_id}, course_average={self.course_average}, best_average={self.best_average}, {self.qualify}'
        return self.step5()
    
    def step5(self):
        if self.course_average >= 65 and self.course_average<=70 and self.best_average<80:
            return f'id={self.person_id}, course_average={self.course_average}, best_average={self.best_average}, MAY HAVE A GOOD CHANCE! Need further assessment'
        return self.step6()
    
    def step6(self):
        if self.course_average<65 and self.course_average>=60 and self.best_average>=80:
            return f"id={self.person_id}, course_average={self.course_average}, best_average={self.best_average}, MAY HAVE GOOD CHANCE! Must be carefully reassessed and get coordinator's permission!"
        return f'id={self.person_id}, course_average={self.course_average}, {self.disqualify}'


def evaluate(unit_scores:UnitScores,person_id):
    """
    Evaluate students based on their unit scores
    returns a message with the results of the evaluation
    """
    display_unit_scores(unit_scores)
    evaluation = EvaluationPipeline(unit_scores,person_id)
    return evaluation.evaluate()

proxy = client.ServerProxy('http://localhost:8000/RPC2')

def authenticate(student_id:int, password:str)->str:
    """
    Authenticate students using their student_id and their firstname as password
    """
    return proxy.confirm_credentials(student_id,password)

def register(firstname:str, lastname:str)->int:
    """
    Register non students.
    Takes firstname and lastname
    returns student_id as an integer
    """
    pass

def student_assessment(student_id:int,password:str):
    if authenticate(student_id,password):
        unit_scores = proxy.get_unit_scores(student_id)
        return evaluate(unit_scores,student_id)
    
def non_student_assessment(person_id:int,unit_scores:list):
    return evaluate(unit_scores,person_id)


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',5000),requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    server.register_function(student_assessment)
    server.register_function(student_assessment)
    server.serve_forever()
