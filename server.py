import socket, ast
from threading import Thread
from datetime import datetime


LISTENING_PORT = 8080

connections = []

def handle_user_connection(connection: socket.socket, address: str):
    while True:  
            msg = connection.recv(1024)

            if msg:
                dict_msg = ast.literal_eval(msg.decode())

                msg_to_send = ''

                match(dict_msg['action']):
                    case 'send_message':
                        date_formatted = datetime.fromisoformat(dict_msg["sended_at"]).strftime("%m/%d/%Y, %H:%M:%S")
                        msg_to_send = f'\n \033[0;31m{dict_msg["user"]}:{date_formatted}\n \033[1;37m {dict_msg["message"]}\n'
                    case 'join_chat':
                        msg_to_send = f'\n \033[1;32m {dict_msg["user"]} from {address[0]}:{address[1]} just join the chat!'

                broadcast(msg_to_send, connection)                
            else:
                break


def broadcast(message: str, user_connection: socket.socket):
    for client_conn in connections:
        if client_conn != user_connection:
                client_conn.send(message.encode())



def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.bind(('', LISTENING_PORT))
        conn.listen(10)
        print('Server running')
        while True:
            socket_connection, address = conn.accept()
            connections.append(socket_connection)
            Thread(target=handle_user_connection, args=[socket_connection, address]).start()
            

if __name__ == "__main__":
    server()