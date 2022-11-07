import random
import json
res = {}
res["COUNT"] = 0
def new_task(text, answ):
    res["COUNT"] += 1
    res[f"T_{res['COUNT']}_TEXT"] = text
    res[f"T_{res['COUNT']}_ANSW_CORRECT"] = answ
########################################################################


# 1
a = random.randint(72,255)
T_TEXT = f'''Переведите число <b>из двоичной с.с. в десятичную с.с.</b><br><br>
{bin(a)[2:]}<br><br>'''
T_ANSW_CORRECT = f"{a}"
new_task(T_TEXT, T_ANSW_CORRECT)

# 2
a = random.randint(72,255)
T_TEXT = f'''Переведите число <b>из восьмеричной с.с. в десятичную с.с.</b><br><br>
{oct(a)[2:]}<br><br>'''
T_ANSW_CORRECT = f"{a}"
new_task(T_TEXT, T_ANSW_CORRECT)

# 3
a = random.randint(72,255)
T_TEXT = f'''Переведите число <b>из шестнадцатеричной с.с. в десятичную с.с.</b><br><br>
{hex(a).upper()[2:]}<br><br>'''
T_ANSW_CORRECT = f"{a}"
new_task(T_TEXT, T_ANSW_CORRECT)



########################################################################
print(json.dumps(res, indent=4, ensure_ascii=True, sort_keys=False))
