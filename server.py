import socket
import threading
import base64
import time

# Dictionary to store client connections
clients = {}
groups = {}
channels = {}

def handle_client(client, username):
    while True:
        try:
            # Receive encrypted message
            encrypted_message = client.recv(1024).decode()
            if encrypted_message:
                # Decrypt the message
                decrypted_message = base64.b64decode(encrypted_message.encode()).decode()
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{current_time}] ({username}): {decrypted_message}")

                # Check if message is a command
                if decrypted_message.startswith('/'):
                    parts = decrypted_message.split(maxsplit=1)
                    command = parts[0]
                    print(command)
                    if command == '/groupcreate':
                        if len(parts) > 1:
                            group_name = parts[1]
                            create_group(client, group_name)
                        else:
                            client.send("Usage: /groupcreate group_name".encode())

                    elif command == '/groupjoin':
                        if len(parts) > 1:
                            group_name = parts[1]
                            join_group(client, group_name)
                        else:
                            client.send("Usage: /groupjoin group_name".encode())
                    elif command == '/groupleave':
                        if len(parts) > 1:
                            group_name = parts[1]
                            leave_group(client, group_name)
                        else:
                            client.send("Usage: /groupleave group_name".encode())

                    elif command == '/channelcreate':
                        if len(parts) > 1:
                            channel_name = parts[1]
                            create_channel(client, channel_name)
                        else:
                            client.send("Usage: /channelcreate channel_name".encode())

                    elif command == '/channeljoin':
                        if len(parts) > 1:
                            channel_name = parts[1]
                            join_channel(client, channel_name)
                        else:
                            client.send("Usage: /channeljoin channel_name".encode())
                    elif command == '/channelleave':
                        if len(parts) > 1:
                            channel_name = parts[1]
                            leave_channel(client, channel_name)
                        else:
                            client.send("Usage: /channelleave channel_name".encode())
                    # Check if message is for a group
                    elif command.startswith('/group'):
                        if len(parts) >1:
                            args=parts[1].split(maxsplit=1)
                            if len(args) >1:

                                group_name, group_message = args[0], args[1]

                                send_to_group(client, group_name, group_message)
                            else:
                                client.send("Usage: /group group_name message".encode())
                        else:
                            client.send("Usage: /group group_name message".encode())

                    # Check if message is for a channel
                    elif command.startswith('/channel'):

                        if len(parts) > 1:
                            args = parts[1].split(maxsplit=1)
                            if len(args)>1:
                                channel_name, channel_message = args[0], args[1]
                                send_to_channel(client, channel_name, channel_message)
                            else:
                                client.send("Usage: /channel channel_name message".encode())
                        else:
                            client.send("Usage: /channel channel_name message".encode())
                

                    elif command.startswith('/message'):
                        # Broadcast the message to all clients except the sender
                        message=f"[{current_time}] ({username}): {decrypted_message.split(maxsplit=1)[1]}".encode()
                        # print(message)
                        for client_socket in clients:
                            if client_socket != client:
                                client_socket.send(message)
        except:
            # If an error occurs, remove the client and close the connection
            print(f"Connection with {username} closed.")
            client.close()
            del clients[client]
            break

def create_group(client, group_name):
    groups[group_name] = {
        'owner':client,
        'members': [clients[client]],
        'clients': [client]
    }
    client.send(f"Group '{group_name}' created successfully.".encode())

def join_group(client, group_name):
    if group_name in groups:
        groups[group_name]['members'].append(clients[client])
        groups[group_name]['clients'].append(client)
        client.send(f"Joined group '{group_name}' successfully.".encode())
    else:
        client.send(f"Group '{group_name}' does not exist.".encode())
def leave_group(client, group_name):
    if group_name in groups:
        if clients[client] in groups[group_name]['members']:
            groups[group_name]['members'].remove(clients[client])
            groups[group_name]['clients'].remove(client)
            client.send(f"Left group '{group_name}' successfully.".encode())
        else:
            client.send("You are not a member of this group.".encode())
    else:
        client.send(f"Group '{group_name}' does not exist.".encode())

def create_channel(client, channel_name):
    channels[channel_name] = {
        'owner':client,
        'members': [clients[client]],
        'clients': [client]
    }
    client.send(f"Channel '{channel_name}' created successfully.".encode())

def join_channel(client, channel_name):
    if channel_name in channels:
        channels[channel_name]['members'].append(clients[client])
        channels[channel_name]['clients'].append(client)
        client.send(f"Joined channel '{channel_name}' successfully.".encode())

    else:
        client.send(f"Channel '{channel_name}' does not exist.".encode())
    
def leave_channel(client, channel_name):
    if channel_name in channels:
        if clients[client] in channels[channel_name]['members']:
            channels[channel_name]['members'].remove(clients[client])
            channels[channel_name]['clients'].remove(client)
            client.send(f"Left channel '{channel_name}' successfully.".encode())
        else:
            client.send("You are not a member of this channel.".encode())
    else:
        client.send(f"Channel '{channel_name}' does not exist.".encode())

def send_to_group(sender_client, group_name, message):
    if group_name in groups:
        if sender_client in groups[group_name]['clients']:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            sender_name = clients[sender_client]
            for client_socket in groups[group_name]['clients']:
                if client_socket != sender_client:
                    client_socket.send(f"[{current_time}] ({sender_name}{' (owner)' if sender_client==groups[group_name]['owner'] else ''} in {group_name}): {message}".encode())
        else:
            sender_client.send(f"You are not a member of Group '{group_name}'!".encode())
    else:
        sender_client.send(f"Group '{group_name}' does not exist.".encode())

def send_to_channel(sender_client, channel_name, message):

    if channel_name in channels:
        if channels[channel_name]['owner']==sender_client:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            sender_name = clients[sender_client]
            for client_socket in channels[channel_name]['clients']:
                if client_socket != sender_client:
                    client_socket.send(f"[{current_time}] ({sender_name} in {channel_name}): {message}".encode())
        else :
                    sender_client.send(f"You are not allowed to send message in Channel '{channel_name}'".encode())

    else:
        sender_client.send(f"Channel '{channel_name}' does not exist.".encode())

def main():
    host = "127.0.0.1"
    port = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    server.listen()

    print("Server is running on ",host,":",str(port))

    while True:
        client, addr = server.accept()
        print(f"Connection established with {addr}")

        # Receive username from client
        username = client.recv(1024).decode()
        clients[client] = username

        # Start a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client, username))
        client_thread.start()

if __name__ == "__main__":
    main()
