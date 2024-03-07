import socket
import base64
import threading
import time
import re

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if (message.startswith('[')):
                # Regex pattern to match any text after the colon
                pattern = r"\[.*\] \(.*\): (.*)"


                # Using search() to find the first occurrence of the pattern
                match = re.search(pattern, message)

                # Extracting the message
                data = match.group(1) if match else "None"

                decrypted_data = base64.b64decode(data.encode()).decode()

                message=message.replace(data,decrypted_data)
                
            
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
        if message.startswith('/'):
                try:
                    parts = message.split(maxsplit=1)
                    command = parts[0]
                    if command=='/group' or command=='/channel':
                         message_parts=parts[1].split(maxsplit=1)
                         name=message_parts[0]
                         data=message_parts[1]
                         encrypted_data=base64.b64encode(data.encode()).decode()
                         message=message.replace(data, encrypted_data)
                except:
                    print('wrong command  usage')


        else:
            encrypted_data = base64.b64encode(message.encode()).decode()
            message = "/message "+encrypted_data
             
                    

        encrypted_message = base64.b64encode(message.encode()).decode()
        # print('message ',encrypted_data)
        client.send(encrypted_message.encode())


if __name__ == "__main__":
    main()
