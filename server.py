import json
import socket

from config import CONNECTION


class Server(socket.socket):
    def __init__(self, **kwargs) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM, **kwargs)


def start_server():

    server = Server()

    try:
        server.bind(CONNECTION)
        server.listen(1)
        print("Server started")
    except:
        print('Server already started')
        server.close()
        exit(0)

    while True:

        print("Waiting for connection...")
        (clientConnection, clientAddress) = server.accept()
        print("The client connected:", clientAddress)
        msg = ''

        while True:

            in_data = clientConnection.recv(1024)
            msg = in_data.decode()
            data = json.loads(msg)

            answer = None

            if data["command"] == 'bye':
                print("The client disconnected....")
                clientConnection.close()
                break

            if data["command"] == 'stop':
                print("Server turns off")
                clientConnection.close()
                server.close()
                exit(0)

            if data["command"] == 'add':
                print("Adds a book")
                answer = add_book(data["object"])

            if data["command"] == 'del':
                print("Removes a book")
                answer = del_book(data["object"])

            if data["command"] == 'read':
                print("Reads a book list")
                answer = read_books()

            clientConnection.send(bytes(json.dumps(answer), 'UTF-8'))



def del_book(id):
    content = read_books()

    if id in content:
        del content[id]
        save_books(content)
        return "Book was removed"
    
    return "Book doesn't exists"


def add_book(book):
    msg=check_book(book)

    if msg:
        return msg
        
    content=read_books()
    id=int(get_max_id(content)) + 1
    content[id]=book
    
    save_books(content)

    return "Book was added"


def check_book(book):
    if book['author'].isdigit():
        return "The name of author contains a digits!"

    if not book['pages'].isdigit():
        return "The pages contains a text!"

    return ""


def read_books():
    import os

    if os.path.isfile("books.json"):
        with open('books.json', 'r') as f:
            return json.loads(f.read())
    
    return {}


def get_max_id(content):
    if content:
        return max(content.keys())

    return 0


def save_books(content):
    with open('books.json', 'wt') as f:
        f.write(json.dumps(content))


start_server()