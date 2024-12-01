import socket
import threading

HOST = '10.60.135.42'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []  # (username, client)

# Function to send user list to all clients
def send_user_list():
    users = [user[0] for user in active_clients]
    for user in active_clients:
        try:
            user_list = "SERVER~" + ",".join(users)
            send_message_to_client(user[1], user_list)
        except Exception as e:
            print(f"Failed to send user list to {user[0]: {e}}")

# Function to listen for messages from a client
def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                recipient, content = message.split("~", 1)
                send_message_to_specific_client(recipient, username, content)
            else:
                print(f"Empty message from {username}")
                remove_client(client)
                break
        except Exception as e:
            print(f"Connection lost with {username}:{e}")
            remove_client(client)
            break

# Function to send message to a specific client
def send_message_to_specific_client(recipient, sender, message):
    for user in active_clients:
        if user[0] == recipient:
            try:
                send_message_to_client(user[1], f"{sender}~{message}")
            except Exception as e:
                print(f"Failed to send message to {recipient}:{e}")
                remove_client(user[1])

# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to remove a client from active_clients
def remove_client(client):
    for user in active_clients:
        if user[1] == client:
            active_clients.remove(user)
            break
    client.close()
    send_user_list()  # Update user list when a client disconnects

# Function to handle client connections
def client_handler(client):
    try:
        username = client.recv(2048).decode('utf-8')
        if username:
            active_clients.append((username, client))
            send_user_list()  # Send updated user list to everyone
            threading.Thread(target=listen_for_messages, args=(client, username)).start()
        else:
            remove_client(client)
    except Exception as e:
        print(f"Error handling client {e}")
        remove_client(client)

# Main function to start the server
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Server running on {HOST}:{PORT}")
    except:
        print(f"Unable to bind to {HOST}:{PORT}")
        return

    server.listen(LISTENER_LIMIT)
    print("Listening for connections...")



    while True:
        try:
            client, address = server.accept()
            print(f"Connected to {address}")
            threading.Thread(target=client_handler, args=(client,)).start()
        except Exception as e:
            print(f"Error accepting connections: {e}")

if __name__ == '__main__':
    main()
