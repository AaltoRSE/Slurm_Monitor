from typing import Type, Any
class DBJob:
    def __init__(self, db_result, headers):
        # print(headers)
        # print(db_result)
        self.headers = headers
        self.result = list(db_result)
        self.value_dict = {}
        for index,field in enumerate(headers):
            if index < len(self.result):
                self.value_dict[field] = self.result[index]

    def get(self, field : str, return_type : Type = str, default = None) -> Any:
        try:
            value = self.value_dict[field]
            return return_type(value) if not value is None else default
        except:
            return default
                
    def set(self, field : str, value : Any):
        self.value_dict[field] = value            