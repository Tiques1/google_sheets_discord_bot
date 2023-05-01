import sys

import gspread
import configparser
from gspread import Worksheet, Client, Spreadsheet

config = configparser.ConfigParser()
config.read('apikeys.cfg.txt')


def conf(server_id, name = None):
    config.read('apikeys.cfg.txt')
    gc: Client = gspread.service_account("./sheet_api.json")
    sh: Spreadsheet = gc.open_by_url(config[server_id]['SHEETURL'])
    if name != None:
        return sh.worksheet(name)
    return sh.worksheet(config[server_id]['USER_NAME'])


def punishment_history(line1, server_id):
    s = conf(server_id, 'punishment_history')
    s.append_rows([line1])

def file_update(members, server_id): # у меня всего 60 запросов в минуту, выкручивался как мог
    s = conf(server_id)
    s.batch_clear(['A:E'])
    i = 0
    length = len(members)
    if length % 2 == 1:
        s.append_row(members[i])
        i += 1
        length -= 1

    digits = [0, 0, 0, 0, 0]  # 10, 8, 4, 2
    while length > 0:
        if length - 10 >= 0:
            digits[0] += 1
            length -= 10
            continue
        if length - 8 >= 0:
            digits[1] += 1
            length -= 8
            continue
        if length - 4 >= 0:
            digits[2] += 1
            length -= 4
            continue
        if length - 2 >= 0:
            digits[3] += 1
            length -= 2
            continue
    file_writing(members, i, digits, s)


def file_writing(members, i, digits: list, s):
    j = digits[0]
    while j > 0:
        s.append_rows(
            [members[i], members[i + 1], members[i + 2], members[i + 3], members[i + 4], members[i + 5], members[i + 6],
             members[i + 7], members[i + 8], members[i + 9]])
        i += 10
        j -= 1
    j = digits[1]
    while j > 0:
        s.append_rows(
            [members[i], members[i + 1], members[i + 2], members[i + 3], members[i + 4], members[i + 5], members[i + 6],
             members[i + 7]])
        i += 8
        j -= 1
    j = digits[2]
    while j > 0:
        s.append_rows([members[i], members[i + 1], members[i + 2], members[i + 3]])
        i += 4
        j -= 1
    j = digits[3]
    while j > 0:
        s.append_rows([members[i], members[i + 1]])
        i += 2
        j -= 1


def delete(member_id, server_id):
    s = conf(server_id)
    s.delete_row(s.find(member_id).row)


def append(member, server_id):
    s = conf(server_id)
    if s.find(member[0]) is None:
        s.append_rows([member])

