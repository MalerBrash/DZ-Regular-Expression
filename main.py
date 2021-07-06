# from pprint import pprint
import csv
import re


def get_list(*arg):  # генератор исправленных вложенных списков первичного списка
    under_list = []
    for i in range(len(arg[-1])):
        if len(arg[i]) == 0 and i == (len(under_list)):
            under_list.append('')
        elif len(arg[i]) == 1:
            under_list.append(arg[i][0])
        elif len(arg[i]) == 2:
            under_list.append(arg[i][0])
            under_list.append(arg[i][1])
        elif len(arg[i]) == 3:
            under_list.append(arg[i][0])
            under_list.append(arg[i][1])
            under_list.append(arg[i][2])
    return under_list


def start():  # читаем адресную книгу в формате CSV в список
    with open(FILE, "r",  encoding="utf-8", newline="") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    get_full_list(contacts_list)


def write_csv(list):  # пишем исправленную адресную книгу в формате CSV
    with open(FILE, "w", encoding="utf-8", newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list)


def get_full_list(list):  # генератор исправленного списка для адресной книги
    title = list.pop(0)
    raw_list = []
    names_list = []
    check_list = []
    for i, val in enumerate(list):
        res_l_name = PATTERN.findall(val[0])
        res_f_name = PATTERN.findall(val[1])
        res_surname = PATTERN.findall(val[2])
        res_org = PATTERN.findall(val[3])
        res_pos = PATTERN1.findall(val[4])
        res_tel = re.sub(PATTERN_PHONE, SUBSTITUTION, val[5])
        res_mail = PATTERN_MAIL.findall(val[6])
        list_tel = [res_tel.strip()]
        element_list = get_list(res_l_name, res_f_name, res_surname, res_org, res_pos, list_tel, res_mail, val)
        repiat = [element_list[0], element_list[1]]

        if repiat not in names_list:
            names_list.append(repiat)
        else:
            check_list.append(i)

        raw_list.append(element_list)

    full_list = raw_list.copy()
    finish_list = find_overlap(full_list, raw_list, check_list)
    finish_list.insert(0, title)
    write_csv(finish_list)


def find_overlap(list, raw_list, check_list):  # ищем и удаляем повторы в списке
    overlaps = []
    for i, v in enumerate(list):
        result = PATTERN.findall(v[0])
        result1 = PATTERN.findall(v[1])
        for val in check_list:
            result2 = PATTERN.findall(list[val][0])
            result3 = PATTERN.findall(list[val][1])
            if result == result2 and result1 == result3 and i != val:
                try:
                    raw_list.remove(v)
                    raw_list.remove(list[val])
                except ValueError:
                    print(f'Неудалось удалить:{v} или {list[val]}')
                fall = []
                for num in range(len(v)):
                    if v[num] == '' and list[val][num] == '':
                        fall.append(v[num])
                    elif v[num] == '' and list[val][num] != '':
                        fall.append(list[val][num])
                    elif list[val][num] == '' and v[num] != '':
                        fall.append(v[num])
                    elif v[num] == list[val][num]:
                        fall.append(v[num])

                overlaps.append(fall)
    return raw_list + overlaps


PATTERN = re.compile(r"[а-яёА-ЯЁ]+")
PATTERN1 = re.compile(r".+")
PATTERN_PHONE = r"(\+7|8|7)?\s*[\(]*(\d{3})[\)-]*\s*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*\(*(доб\.)\s*(\d+)\)*)?"
PATTERN_MAIL = re.compile(r"\w+\.*\w+\@\w+\.\w+")
SUBSTITUTION = r"+7(\2)\3-\4-\5 \7\8"
FILE = "phonebook_raw.csv"

if __name__ == '__main__':
    start()

