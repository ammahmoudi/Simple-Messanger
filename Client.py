import socket
import base64
import threading
import time

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            break

def main():
    host = "127.0.0.1"
    port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    username = input("Enter your username: ")
    client.send(username.encode())

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()

        encrypted_message = base64.b64encode(message.encode()).decode()
        client.send(encrypted_message.encode())


if __name__ == "__main__":
    main()
