import pandas as pd
from base import UnitScores
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler


excel_path = 'demo data.xlsx'

class TableNotFound(Exception):
    pass

class DemoDatabase:
    def __init__(self,dataframes:dict[str,pd.DataFrame]) -> None:
        self.dataframes = dataframes

    def insert(self,table_name:str,**query):
        table = self.dataframes.get(table_name)
        if table:
            new_row = pd.Series([key for key,value in query.items()],index=[key for key in query.keys()])
            table.loc[len(table)] = new_row
        else:
            raise TableNotFound

    def select(self,table_name:str,*columns,**query):
        if table_name in self.dataframes.keys():
            table = self.dataframes.get(table_name)
            for key,value in query.items():
                table = table[table[key]==value]
            if not table.empty:
                selection = table[list(columns)]
                named_tuples = [tuple(row) for row in selection.itertuples(index=False)]
                return named_tuples
            else:
                return None
            
        else:
            raise TableNotFound

    def update(table_name:str,**query):
        pass

    def delete(table_name:str,**query):
        pass

data_frames = pd.read_excel(excel_path,sheet_name=None)
demo_database = DemoDatabase(data_frames)

def confirm_credentials(student_id:int, firstname:str)->bool:
    student = demo_database.select('student_Info','Person_ID',Person_ID=student_id,First_Name=firstname)
    if student:
        return True
    return False

def get_unit_scores(student_id:int):
    unit_scores = demo_database.select('student_unit','Unit_code','Result_Score',Person_ID=student_id)
    return unit_scores

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',8000),requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    server.register_function(confirm_credentials)
    server.register_function(get_unit_scores)
    server.serve_forever()
