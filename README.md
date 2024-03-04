# Simple Chat App with Group and Channel Functionalities

This is a simple chat application implemented in Python using a server-client architecture. The app allows users to create groups, join groups, leave groups, create channels, join channels, leave channels, and send messages to groups and channels.

## Features

- **Server-Client Architecture**: The app is built using a client-server model where multiple clients can connect to a central server.
- **End-to-End Encryption**: Messages sent between clients and the server are encrypted using base64.
- **Timestamps**: Each message is timestamped to indicate when it was sent.
- **Group Management**: Users can create groups, join groups, and leave groups. Messages can be sent to specific groups.
- **Channel Management**: Users can create channels, join channels, and leave channels. Messages can be sent to specific channels.
- **Simple Command Line Interface (CLI)**: The app features a simple CLI for user interaction.
- **Usage of Sockets**: Sockets are used for communication between clients and the server.

## Screenshots

![sc1](/images/sc (1).png)

![sc2](/images/sc (2).png)


## Usage

1. Run `chat_server.py` on your server machine.
2. Run `chat_client.py` on different client machines or multiple times on the same machine.
3. Enter a username for each client.
4. Use commands to create groups, join groups, leave groups, create channels, join channels, leave channels, and send messages to groups and channels.

### Group Commands
- `/groupcreate group_name`: Creates a new group.
- `/groupjoin group_name`: Joins an existing group.
- `/groupleave group_name`: Leaves a group.

### Channel Commands
- `/channelcreate channel_name`: Creates a new channel.
- `/channeljoin channel_name`: Joins an existing channel.
- `/channelleave channel_name`: Leaves a channel.

### Sending Messages
- To send a message to a group: `/group group_name message`
- To send a message to a channel: `/channel channel_name message`

## Requirements

- Python 3.x

## Disclaimer

This chat application is a simplified example intended for educational purposes. It may not be suitable for use in production environments. Use at your own risk.

