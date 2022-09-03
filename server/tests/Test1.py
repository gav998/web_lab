import random
import json
res = {}
res["COUNT"] = 0

messages = ['Не видно, ликвидны акции или неликвидны.',
            'Добры бобры идут в боры.',
            'Звёздный змей звенел зубами: «З-з-з».',
            'Сидели, свистели семь свиристелей.',
            'На лозе оса, в лозе коза.',
            'Связку сушек сушил Саша на суше.',
            'Говорит попугай попугаю: «Я тебя попугаю».',
            'Карл у Клары украл кораллы!',
            'Дарья дарит Дине дыни.',
            'Три сороки-тараторки тараторили на горке.',
            'Жужжит над жимолостью жук, тяжёлый на жуке кожух.',
            'Щуку я тащу, тащу, Щуку я не упущу!',
            'Перепёлка перепелят прятала от ребят.',
            'Учит бегать ёж ужат, учит ползать уж ежат.',
            'Хвост вытащишь – голова увязнет!',
            'Сделал дело — гуляй смело!',
            'Седина в бороду — бес в ребро!',
            'Первый блин — комом!',
            'Не учи учёного.',
            'Плохо овцам, коли волк пастух!',
            'Нет худа без добра!',
            'Что посеешь, то и пожнешь!',
            'Кто в лес, кто по дрова?',
            'На других умён, на себя глуп!',
            'Кот из дому, мыши в пляс!',
            'Глаза боятся, а руки делают!',
            'В бане веник — дороже денег!',
            'Было, да сплыло!']

########################################################################
T_TEXT = ""
res["COUNT"] += 1
#
i = random.randint(1,2)*8
h = random.randint(0,1)*7+1
hs = 'БАЙТ' if h==8 else 'БИТ'
message = random.choice(messages)
T_TEXT += f'''Определите количество <b>{hs}</b> в сообщении, если оно записано в кодировке <b>UTF-{i}</b><br><br>'''
T_TEXT += f'''<p class="font-monospace">{message}</p>'''
T_ANSW_CORRECT = f"{int(len(message)*i/h)}"
#
res[f"T_{res['COUNT']}_TEXT"] = T_TEXT
res[f"T_{res['COUNT']}_ANSW_CORRECT"] = T_ANSW_CORRECT

########################################################################
T_TEXT = ""
res["COUNT"] += 1
#
i = random.randint(1,2)*8
h = random.randint(0,1)*7+1
hs = 'БАЙТ' if h==8 else 'БИТ'
message = random.choice(messages)
T_TEXT += f'''Определите количество <b>{hs}</b> в сообщении, если оно записано в кодировке <b>UTF-{i}</b><br><br>'''
T_TEXT += f'''<p class="font-monospace">{message}</p>'''
T_ANSW_CORRECT = f"{int(len(message)*i/h)}"
#
res[f"T_{res['COUNT']}_TEXT"] = T_TEXT
res[f"T_{res['COUNT']}_ANSW_CORRECT"] = T_ANSW_CORRECT

########################################################################
T_TEXT = ""
res["COUNT"] += 1
#
i = random.randint(1,2)*8
h = random.randint(0,1)*7+1
hs = 'БАЙТ' if h==8 else 'БИТ'
message = random.choice(messages)
T_TEXT += f'''Определите количество <b>{hs}</b> в сообщении, если оно записано в кодировке <b>UTF-{i}</b><br><br>'''
T_TEXT += f'''<p class="font-monospace">{message}</p>'''
T_ANSW_CORRECT = f"{int(len(message)*i/h)}"
#
res[f"T_{res['COUNT']}_TEXT"] = T_TEXT
res[f"T_{res['COUNT']}_ANSW_CORRECT"] = T_ANSW_CORRECT




print(json.dumps(res, indent=4, ensure_ascii=False, sort_keys=False))



