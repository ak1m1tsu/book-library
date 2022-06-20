import socket
import json
from time import sleep

from config import CONNECTION


class Client(socket.socket):
    def __init__(self, **kwargs) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM, **kwargs)
        self.role = 'user'


def start_client():

    client = Client()
    client.connect(CONNECTION)
    print ("Connected to server as User")

    while True:
        
        print("Choose a command")
        print("0 - Get a book list")
        print("1 - Add book")
        print("2 - Remove book")
        print("3 - Exit")
        print("4 - Выключить сервер")

        task = input()

        if not task.isdigit() or int(task) > 4:
            print ("Wrong command!")
            continue

        task=int(task)

        msg = {}

        if task == 0:
            msg["command"] = "read"

        if task == 1:
            msg["command"]= "add"
            msg["object"] = create_book()

        if task == 2:
            msg["command"] = "del"
            msg["object"] = get_id()

        if task == 3:
            msg["command"] = "bye"

        if task == 4:
            msg["command"] = "stop"

        js_string=json.dumps(msg)
        client.sendall(bytes(js_string, 'UTF-8'))

        content={}

        if task < 3:
            in_data = client.recv(1024).decode()

            try:
                content=json.loads(in_data)
            except Exception as error:
                print("Something went wrong: ", error)
                print("Client disconnected...")
                client.close()
                exit(0)

        if task == 0:
            if content:
                print_books(content)
            else:
                print("The list is empty")

        if task == 1:
            print(content)

        if task == 2:
            print(content)

        if task == 3:
            print('Disconnect from server')
            client.close()
            exit(0)

        if task == 4:
            print('Server turns off')
            sleep(1)
            print('Disconnected from server')
            sleep(1)
            client.close()
            exit(0)


def print_books(books):
    print ("="*15)
    print('The book list')
    print ("="*15)
    for id in books.keys():
        print ("%s - %s - %s - %s" % (id, books[id]["name"], books[id]["author"], books[id]["pages"]))
    print ("="*15)


def create_book():
    book={}
    print("Enter a book name:")
    book['name']=input()

    print("Enter a book author:")
    book['author']=input()

    print("Enter page count:")
    book['pages']=input()

    return book


def get_id():
    while True:
        print("Enter book number:")
        id = input()

        if id.isdigit():
            return id

        print ("Incorrect number")


start_client()