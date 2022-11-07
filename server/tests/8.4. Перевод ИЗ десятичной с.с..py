import random
import json
res = {}
res["COUNT"] = 0
def new_task(text, answ):
    res["COUNT"] += 1
    res[f"T_{res['COUNT']}_TEXT"] = text
    res[f"T_{res['COUNT']}_ANSW_CORRECT"] = answ
########################################################################


def iz_10(N, m):
    R = ''
    while(N > 0):
        R = hex(N % m)[2:] + R
        N = N // m
    return R

p = [3,4,5,6,7,9,11,12,13,14,15]

# 1
a = random.randint(72,255)
m = random.choice(p)
T_TEXT = f'''Переведите число <b>из десятичной с.с. в {m} с.с.</b><br><br>
{a}<sub>10</sub><br><br>'''
T_ANSW_CORRECT = f"{iz_10(a, m).upper()}"
new_task(T_TEXT, T_ANSW_CORRECT)

# 2
a = random.randint(72,255)
m = random.choice(p)
T_TEXT = f'''Переведите число <b>из десятичной с.с. в {m} с.с.</b><br><br>
{a}<sub>10</sub><br><br>'''
T_ANSW_CORRECT = f"{iz_10(a, m).upper()}"
new_task(T_TEXT, T_ANSW_CORRECT)

# 3
a = random.randint(72,255)
m = random.choice(p)
T_TEXT = f'''Переведите число <b>из десятичной с.с. в {m} с.с.</b><br><br>
{a}<sub>10</sub><br><br>'''
T_ANSW_CORRECT = f"{iz_10(a, m).upper()}"
new_task(T_TEXT, T_ANSW_CORRECT)

# 4
a = random.randint(72,255)
m = random.choice(p)
T_TEXT = f'''Переведите число <b>из десятичной с.с. в {m} с.с.</b><br><br>
{a}<sub>10</sub><br><br>'''
T_ANSW_CORRECT = f"{iz_10(a, m).upper()}"
new_task(T_TEXT, T_ANSW_CORRECT)

# 5
a = random.randint(72,255)
m = random.choice(p)
T_TEXT = f'''Переведите число <b>из десятичной с.с. в {m} с.с.</b><br><br>
{a}<sub>10</sub><br><br>'''
T_ANSW_CORRECT = f"{iz_10(a, m).upper()}"
new_task(T_TEXT, T_ANSW_CORRECT)


########################################################################
print(json.dumps(res, indent=4, ensure_ascii=True, sort_keys=False))
