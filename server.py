import socket
import random
from threading import Thread

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = "127.0.0.1"
port = 8000
server.bind((ip_address,port))
server.listen()

list_of_clients = []
nicknames = []
print("Server Started!")

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

questions = [
    "What is the largest city in the world? \n a.Wasington \n b.Tokyo \n c.Delhi \n d.Mumbai",
    "When did World War 1 start? \n a.1905 \n b.1814 \n c.1919 \n d.1914",
    "Which alliance was against NATO? \n a.Indo-Soviet Defence Pact \n b.G-7 \n c.BRICS \n d. Warsaw Pact",
    "When did Yugoslavia dissolved? \n a.1992 \n b.1991 \n c.1948 \n d.1980"
    "Which country liberated Berlin during World War 2? \n a.USA \n b.UK \n c.USSR \n d.France"
]
answers = ['b','d','d','a','c']

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode("uft-8"))
    return random_index,random_question,random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def client_thread(conn):
    score = 0
    conn.send("Welcome to this quiz room! \n".encode("utf-8"))
    conn.send("Please answer the following question in a,b,c or d \n".encode("uft-8"))
    conn.send("Good Luck! \n \n".encode("uft-8"))
    index,question,answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.lower() == answer:
                    score+=1
                    conn.send(f"Good! Your score is {score} \n\n".encode("uft-8"))
                else:
                    conn.send("Incorrect! please try again in nect question!")
                remove_question(index)
                index,question,answer = get_random_question_answer(conn)
            else:
                remove(conn)
                remove_nickname(nicknames)
        except:
            continue

def broadcast(message,conn):
    for clients in list_of_clients:
        if clients != conn:
            try:
                clients.send(message.encode("utf-8"))
            except:
                remove(clients)

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)

while True:
    conn,addr = server.accept()
    conn.send("Nickname".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = "{} Joined".format(nickname)
    print(message)
    broadcast(message,conn)
    new_thread = Thread(target=client_thread,args=(conn,addr))
    new_thread.start()