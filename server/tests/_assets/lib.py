import random

def generate_task_1_1():
    '''В одной из кодировок Unicode каждый символ кодируется 32 битами.
зийклмн, ийклмноп, йклмнопрс, клмнопрсту, лмнопрстуфх, мнопрстуфхцч, нопрстуфхцчшщ - некоторые слова на тарабарском языке.
Ученик вычеркнул из списка одно слово. Заодно он вычеркнул ставшие лишними запятые и пробелы - два пробела не должны идти подряд. При этом размер нового предложения в данной кодировке оказался на 60 байт меньше, чем размер исходного предложения.
Напишите в ответе вычеркнутое слово.'''
    ru = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    words = [ru[i:i+i] for i in range(7,14)]
    word = random.choices(words)[0]
    n = len(word)
    i = 2**random.randint(1,2)*8
    answer = word
    task = f"В одной из кодировок Unicode каждый символ кодируется {i} битами.<br><br>"
    task+= f"{', '.join(words)} - некоторые слова на тарабарском языке.<br><br>"
    task+= f"Ученик вычеркнул из списка одно слово. Заодно он вычеркнул ставшие лишними запятые и пробелы - два пробела не должны идти подряд. При этом размер нового предложения в данной кодировке оказался на {int((n+2)*i/8)} байт меньше, чем размер исходного предложения. <br><br>"
    task+= f"Напишите в ответе вычеркнутое слово.<br><br>"
    return task, answer

def generate_task_1_2():
    '''Статья, набранная на компьютере, содержит 16 страницы, на каждой странице 128 строки, в каждой строке 32 символов.
Определите информационный объём статьи в Кбайтах в кодировке UTF-16.'''
    n1 = 2**random.randint(4,6)
    n2 = 2**random.randint(6,8)
    n3 = 2**random.randint(3,8)
    n = n1*n2*n3
    i = 2**random.randint(0,2)*8
    answer = int(n*i/(8*1024))
    task = f"Статья, набранная на компьютере, содержит {n1} страницы, на каждой странице {n2} строки, в каждой строке {n3} символов. <br><br>Определите информационный объём статьи в Кбайтах в кодировке UTF-{i}.<br><br>"
    return task, answer

def generate_task_1_3():
    '''Собрание сочинений, набранное на компьютере, содержит 8 томов, в каждом томе 512 страницы, на каждой странице 256 строки, в каждой строке 128 символов.
Определите информационный объём собрания сочинений в Мбайтах в кодировке UTF-8.'''
    n0 = 2**random.randint(3,3)
    n1 = 2**random.randint(8,10)
    n2 = 2**random.randint(6,8)
    n3 = 2**random.randint(7,8)
    n = n0*n1*n2*n3
    i = 2**random.randint(0,2)*8
    answer = int(n*i/(8*1024*1024))
    task = f"Собрание сочинений, набранное на компьютере, содержит {n0} томов, в каждом томе {n1} страницы, на каждой странице {n2} строки, в каждой строке {n3} символов. <br><br>Определите информационный объём собрания сочинений в Мбайтах в кодировке UTF-{i}.<br><br>"
    return task, answer
    
def generate_task_2_1():
    def decrypt_number(number_str, current_decryption, alphabet, result):
        if len(number_str) == 0:
            result.append(current_decryption)
            return

        single_digit = int(number_str[0])
        if 1 <= single_digit <= 33:
            decrypt_number(number_str[1:], current_decryption + alphabet[single_digit - 1], alphabet, result)

        if len(number_str) >= 2  and number_str[0] != "0":
            double_digit = int(number_str[:2])
            if 1 <= double_digit <= 33:
                decrypt_number(number_str[2:], current_decryption + alphabet[double_digit - 1], alphabet, result)

    def contains_bad_words(text):
        import re
        with open("./tests/_assets/bad_words.txt") as f:
            bad_words_list = [i.rstrip() for i in f]
        pattern = re.compile('|'.join(bad_words_list), re.IGNORECASE)
        match = pattern.search(text)
        return match is not None

    def russian_word_decryptions(encrypted_word):
        alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        result = []
        decrypt_number(encrypted_word, '', alphabet, result)
        return result
        
    def generate_decryption_word(word_length, unique=False):
        alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        while(True):
            unique_word = ''
            for _ in range(word_length):
                while True:
                    unique_word_temp = str(random.randint(1, 33))+unique_word
                    decryptions = russian_word_decryptions(unique_word_temp)
                    if unique and len(decryptions) == 1 or (not unique):
                        break                    
                unique_word = unique_word_temp
            ok = all([(not contains_bad_words(i)) for i in decryptions])
            #ok = any([(contains_bad_words(i, bad_words_list)) for i in decryptions]) #генерируем мат
            if (ok and
               ((unique==False and len(decryptions) > 1) or
               (unique==True and len(decryptions) == 1))):
                break
        return unique_word, decryptions

    pic = './tests/_assets/RU_2.PNG'
    task = f"Ваня шифрует русские слова, записывая вместо каждой буквы её номер в алфавите (без пробелов). Номера букв даны в таблице. <br><br>"
    task+= f'Некоторые шифровки можно расшифровать несколькими способами. Например, 311333 может означать "ВАЛЯ", может — "ЭЛЯ", а может — "ВААВВВ". Даны шифровки:<br><br>'
    words = [generate_decryption_word(7, unique=False)[0] for _ in range(3)]
    word = generate_decryption_word(7, unique=True)
    words.append(word[0])
    answer = word[1][0]
    random.shuffle(words)
    task+= '<br><br>'.join(words)
    task+= f'<br><br>Только одна из них расшифровывается единственным способом. Найдите её и расшифруйте. Получившееся слово запишите в качестве ответа.<br><br>'
    return task, answer, pic


def generate_task_2_2():
    d = {}
    d['О'] = '0'
    d['В'] = '100'
    d['Д'] = '101'
    d['Р'] = '110'
    d['Т'] = '111'
    task = f"Валя шифрует русские слова, записывая вместо каждой буквы её код.<br><br>"
    task+= f"'О' - {d['О']}; "
    task+= f"'В' - {d['В']}; "
    task+= f"'Д' - {d['Д']}; "
    task+= f"'Р' - {d['Р']}; "
    task+= f"'Т' - {d['Т']};<br><br>"
    task+= f"Валя передала Вам следующее сообщение:<br><br>"
    m = ['ВОДОВОРОТВОДООТВОД',
         'ВОДООТВОДВОДОВОД',
         'ВОДООТВОДОТВОДВОРОТ',
         'ВОДОВОРОТДОВОД',
         'ОТВОДОТВОРОТ',
         'ВОДОРОДВОДОВОРОТ',
         'ВОДОРОДВОДОРОД',
        ]
    random.shuffle(m)
    task+= m[0].replace('О',d['О']).replace('В',d['В']).replace('Д',d['Д']).replace('Р',d['Р']).replace('Т',d['Т'])
    task+= f"<br><br>Расшифруйте сообщение и запишите в ответе количество букв в нем.<br><br>"
    answer = f'{len(m[0])}'  
    return task, answer


def generate_task_3_1():
    task = f"Напишите наибольшее натуральное четырёхзначное число x, для которого истинно высказывание:<br><br>"
    d = random.randint(10,100)
    a = random.randint(4000,9999)
    task+= f"НЕ(Первая цифра нечётная) И НЕ(x не делится на {d}) И НЕ(x больше {a})"
    x = -1
    for i in range(9999,999,-1):
        if i//1000%2==0 and i%d==0 and i <= a:
            x = i
            break
    correct = f'{x}'
    return task, correct
    
def generate_task_4_1():
    def create_table_pic(points, roads):
        import uuid
        import pandas as pd
        import matplotlib.pyplot as plt
        data = []
        # Create a DataFrame
        for point1 in points:
            row = []
            for point2 in points:
                if (point1, point2) in roads:
                    row.append(roads[(point1, point2)])
                elif (point2, point1) in roads:
                    row.append(roads[(point2, point1)])
                else:
                    row.append("")
            data.append(row)
        df = pd.DataFrame(data, columns=points, index=points)
        # Plot the table
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.axis('off')
        ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellLoc='center', loc='center', edges='closed')
        name = './tests/_assets/'+str(uuid.uuid4())+'.png'
        plt.savefig(name, dpi=300, bbox_inches='tight')
        plt.close()
        return name

    points = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    roads = {
        ('A', 'B'): 2*random.randint(21, 24),
        ('A', 'C'): 2*random.randint(21, 24),
        ('A', 'D'): 2*random.randint(21, 24),
        ('A', 'E'): 2*random.randint(21, 24),
        ('A', 'G'): 6 * random.randint(20, 21),
        ('B', 'F'): 2*random.randint(21, 24),
        ('B', 'G'): 4 * random.randint(18, 19),
        ('C', 'F'): 2*random.randint(21, 24),
        ('D', 'F'): 2*random.randint(21, 24),
        ('E', 'F'): 2*random.randint(21, 24),
        ('F', 'G'): 2*random.randint(21, 24),
    }
    task = f"Между населёнными пунктами A, B, C, D, E, F, G построены дороги, протяжённость которых приведена в таблице.<br><br>"
    task+= f"Определите длину кратчайшего пути между пунктами A и G, проходящего через пункт F.<br><br> Передвигаться можно только по дорогам, указанным в таблице."
    pic = create_table_pic(points, roads)
    
    options = [
        roads[('A', 'B')] + roads[('B', 'F')] + roads[('F', 'G')],
        roads[('A', 'C')] + roads[('C', 'F')] + roads[('F', 'G')],
        roads[('A', 'D')] + roads[('D', 'F')] + roads[('F', 'G')],
        roads[('A', 'E')] + roads[('E', 'F')] + roads[('F', 'G')],
    ]
    answer = min(options)
    return task, answer, pic





def generate_task_7_ip(num_of_parts):
    def get_parts_IPv4(correct_IPv4, num):
        l = len(correct_IPv4)
        div = l // num
        parts = [correct_IPv4[i*div:(i+1)*div] for i in range(num)]
        if l%num != 0:
            parts.append(correct_IPv4[div*num:])
        random.shuffle(parts)
        return parts

    def IPv4_is_correct(IPv4):
        # print(IPv4)
        parts = IPv4.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not (part.isnumeric() and 0<=int(part)<=255):
                return False
        # print('+', IPv4)
        return True        

    def only_one_permutations_correct(parts):    
        import itertools
        perm_set = itertools.permutations(parts)
        c = 0
        for p in perm_set:
            if IPv4_is_correct(''.join(p)):
                c += 1           
        if c == 1:
            return True
        return False


    while True:
        # print('======================')
        correct = f'{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}'
        # print(T_ANSW_CORRECT)
        parts = get_parts_IPv4(correct, num_of_parts)
        # print(parts)
        if only_one_permutations_correct(parts):
            break
    test = f"Ниже приведены части ip-адреса, cоставьте правильный ip-адрес из этих частей и запишите его в ответ.<br><br>"
    for part in parts:
        test+= part+'<br><br>'
    return test, correct




def generate_task_7_file():
    def get_key(d, value):
        for k, v in d.items():
            if v == value:
                return k

    protocols = ["https", "http", "ftp"]
    second_level_domains = ["color", "box"]
    top_level_domains = [".com", ".io"]
    file_names = ["image", "picture"]
    file_extensions = [".jpg", ".png", ".bmp"]
    folders = ["green", "yellow"]
    spec_sym = [":","/"]
    
    old_protocol = random.choice(protocols)
    old_second_level_domain = random.choice(second_level_domains)
    old_top_level_domain = random.choice(top_level_domains)
    old_folder = random.choice(folders)
    file_name = random.choice(file_names)
    file_extension = random.choice(file_extensions)

    new_protocol = random.choice(protocols)
    new_second_level_domain = random.choice(second_level_domains)
    new_top_level_domain = random.choice(top_level_domains)

    old_domain = f"{old_second_level_domain}{old_top_level_domain}"
    new_domain = f"{new_second_level_domain}{new_top_level_domain}"
    full_file_name = f"{file_name}{file_extension}"

    old_url = f"{old_protocol}://{old_domain}/{old_folder}/{full_file_name}"
    new_url = f"{new_protocol}://{new_domain}/{full_file_name}"
    
    

    all_elements = protocols + second_level_domains + top_level_domains + file_names + file_extensions + folders + spec_sym
    url_codes = {index + 1: element for index, element in enumerate(all_elements)}

    answer = (f"{get_key(url_codes, new_protocol)}"
              f"{get_key(url_codes, ':')}"
              f"{get_key(url_codes, '/')}"
              f"{get_key(url_codes, '/')}"
              f"{get_key(url_codes, new_second_level_domain)}"
              f"{get_key(url_codes, new_top_level_domain)}"
              f"{get_key(url_codes, '/')}"
              f"{get_key(url_codes, file_name)}"
              f"{get_key(url_codes, file_extension)}")
    # for part, code in url_codes.items():
        # if code in new_url:
            # answer += str(part)

    task = f"Файл {full_file_name} был выложен в Интернете по адресу {old_url}. Потом его переместили в корневой каталог на сайте {new_domain}, доступ к которому осуществляется по протоколу {new_protocol}. Имя файла не изменилось.<br><br>"
    task += "Фрагменты нового и старого адресов файла закодированы цифрами от 1 до {}. Запишите последовательность этих цифр, кодирующую адрес файла в сети Интернет после перемещения.<br><br>".format(len(url_codes))
    
    for code, value in url_codes.items():
        task += f"{code}){value}<br><br>"

    return task, answer    

def generate_task_5_1():
    '''У исполнителя Программист две команды, которым присвоены номера:
1. добавь 1
2. умножь на Х
Первая из них увеличивает число на экране на 1, вторая умножает число на Х. Известно, что алгоритм 11211 получает из числа 3 число 22. Найдите Х. Если таких чисел несколько, запишите наибольшее.'''
    a = random.randint(1,3)
    c1 = random.randint(1,3)
    c2 = random.randint(2,7)
    b = (a+c1+c1)*c2+c1+c1
    task = f"У исполнителя Программист две команды, которым присвоены номера:<br><br>"
    task+= f"1. добавь {c1}<br><br>"
    task+= f"2. умножь на Х<br><br>"
    task+= f"Первая из них увеличивает число на экране на {c1}, вторая умножает число на Х. Известно, что алгоритм 11211 получает из числа {a} число {b}. Найдите Х. Если таких чисел несколько, запишите наибольшее.<br><br>"
    answer = f'{c2}'
    return task, answer   

def generate_task_6_1():
    task = f"Ниже приведена программа, записанная на пяти языках программирования.<br><br>"
    pic = './tests/_assets/6.PNG'
    task+= f"Было проведено 9 запусков программы, при которых в качестве значений переменных s и k вводились следующие пары чисел:<br><br>"
    ps = [(random.randint(-10,15), random.randint(6,15)), # +
         (random.randint(-10,-7), random.randint(6,15)),  # +
         (random.randint(-10,-7), random.randint(-10,5)), # -
         (random.randint(-10,-7), random.randint(-10,5)), # -
         (random.randint(-10,-7), random.randint(-10,5)), # -
         (random.randint(-10,-7), random.randint(-10,5)), # -
         (random.randint(-7,3), random.randint(-10,5)), # этот
         (random.randint(5,10), random.randint(-10,5)),   # +-
         (random.randint(5,10), random.randint(-10,5)),]  # +-
    random.shuffle(ps)
    s = ''
    for p in ps:
        s = s + f'({p[0]}, {p[1]}); '
    task+= s
    answer = ''
    
    for a in range(-10, 15):
        c = 0
        for p in ps:
            if not(p[0] > a or p[1] > 5):
                c = c+1
        # print(var,a,c)
        if c == 5:
            answer = f'{a}' 
            break
    task+= '<br><br>Укажите минимальное целое значение параметра А, при котором для указанных входных данных программа напечатает «НЕТ» 5 раз.<br><br>'
    return task, answer, pic


def iz_10(N, m):
    R = ''
    while(N > 0):
        R = hex(N % m)[2:] + R
        N = N // m
    return R
