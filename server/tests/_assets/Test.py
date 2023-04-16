import json

class Test:
    '''Класс теста'''
    def __init__(self):
        self.test = {}
        self.test['COUNT'] = 0
    
    def new_task(self, text, answ, pic=None):
        self.test["COUNT"] += 1
        num = self.test["COUNT"]
        self.test[f"T_{num}_TEXT"] = text
        self.test[f"T_{num}_ANSW_CORRECT"] = answ
        self.test[f"T_{num}_PIC"] = pic
        return True

    def get_task(self, num):
        return self.test[f"T_{num}_TEXT"], \
               self.test[f"T_{num}_ANSW_CORRECT"], \
               self.test[f"T_{num}_PIC"]
        
    def __str__(self):
        return json.dumps(self.test, indent=4, ensure_ascii=True, sort_keys=False)
