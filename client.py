import socket
from threading import Thread
from datetime import datetime

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8080



def handle_received_messages(connection: socket.socket):
    print("Receiving message")
    while True:
            msg = connection.recv(1024)
            
            if msg:
                print(msg.decode())
            else:
                break


def handle_send_messages(msg: str, name: str, action: str, conn: socket.socket):
    message  = {'user': name, 'message': msg, 'sended_at': datetime.now().isoformat(), 'action': action }
    conn.send(str(message).encode())


def client():
    print("Insert your name bellow:")
    name = input()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            conn.connect((SERVER_ADDRESS, SERVER_PORT))
            print('Connected to chat on {0}:{1}'.format(SERVER_ADDRESS, SERVER_PORT))

            handle_send_messages("", name, "join_chat", conn)

            Thread(target=handle_received_messages, args=[conn]).start()

            while True:
                print('\033[0;35m')
                msg = input()
                handle_send_messages(msg, name, "send_message", conn)  

    except Exception as e:
        print("Unexpected error: {0}".format(e))


if __name__ == "__main__":
    client()
