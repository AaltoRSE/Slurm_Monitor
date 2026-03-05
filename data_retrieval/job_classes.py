from typing import Type, Any
class DBJob:
    def __init__(self, db_result, headers):
        # print(headers)
        # print(db_result)
        self.headers = headers
        self.result = db_result

    def get(self, field : str, return_type : Type = str, default = None) -> Any:
        try:
            value = self.result[self.headers[field]]
            return return_type(value) if not value is None else default
        except:
            return default
                
    def set(self, field : str, value : Any):
        if field in self.headers:
            self.result[self.headers[field]] = value
        else:
            self.result.append(value)    
            self.headers[field] = len(self.result) - 1