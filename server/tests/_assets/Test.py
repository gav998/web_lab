import json
import random

class Test:
    '''Класс теста'''
    def __init__(self):
        self.test = {}
        self.tasks = []

        self.test['COUNT'] = 0
    
    def new_task(self, text, answ, pic=None):
        self.test["COUNT"] += 1
        self.tasks.append((text, answ, pic))
        return True
    
    def shuffle(self):
        random.shuffle(self.tasks)
        return True

    def get_task(self, num):
        return self.test[f"T_{num}_TEXT"], \
               self.test[f"T_{num}_ANSW_CORRECT"], \
               self.test[f"T_{num}_PIC"]
        
    def __str__(self):
        for num, task in enumerate(self.tasks):
            text, answ, pic = task
            self.test[f"T_{num+1}_TEXT"] = text
            self.test[f"T_{num+1}_ANSW_CORRECT"] = answ
            self.test[f"T_{num+1}_PIC"] = pic
        return json.dumps(self.test, indent=4, ensure_ascii=True, sort_keys=False)
