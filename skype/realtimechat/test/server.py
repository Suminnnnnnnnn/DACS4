import socket
import threading
import time
#Server
HOST = '0.0.0.0'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []  # (user_id,user_name, client)


def listen_for_messages(client, user_id,address):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            print(message)
            if '~' in message:
                if 'typing' in message:
                    time.sleep(1)
                    parts = message.split('~')
                    if len(parts) == 3:
                        recive,typ,username=message.split('~')
                        send_message_to_specific_client(recive, user_id,username, typ)
                    else:
                        print("Invalid message")
                elif 'CALL_REQUEST' in message:
                    recive,address,message=message.split('~')
                    send_address_to_peer(recive,user_id ,address, "CALL_REQUEST")
                elif 'MESSAGE_GROUP' in message:
                    recive,address,message=message.split('~')
                    send_address_to_peer(recive,user_id ,address, "MESSAGE_GROUP")
                else:
                    recipient, content, user_name = message.split('~')
                    send_message_to_specific_client(recipient, user_id, user_name, content)

            else :
                print(f"Empty message from {user_id}")
                remove_client(client)
                break


        except Exception as e:
            print(f"Connection lost with {user_id}:{e}")
            remove_client(client)
            break
def listen_for_messages_group(client,user_id,array):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            print(message)
            if '~' in message:
                if 'typing' in message:
                    recive, typ, username = message.split('~')
                    send_message_to_specific_client(recive, user_id, username, typ)
                elif 'CALL_REQUEST' in message:
                    recive, address, message = message.split('~')
                    send_address_to_peer(recive, user_id, address, "CALL_REQUEST")
                else:
                    recipient, content, user_name = message.split('~')
                    send_message_to_specific_client(recipient, user_id, user_name, content)

            else:
                print(f"Empty message from {user_id}")
                remove_client(client)
                break


        except Exception as e:
            print(f"Connection lost with {user_id}:{e}")
            remove_client(client)
            break
# Function to send message to a specific client
def send_message_to_specific_client(recipient, sender,name, message):
    for user in active_clients:
        if user[0] == recipient :
            try:
                send_message_to_client(user[2], f"{name}~{recipient}~{message}")
            except Exception as e:
                print(f"Failed to send message to {recipient}:{e}")
                remove_client(user[1])
def send_address_to_peer(recipient, sender,address, message):
    for user in active_clients:
        if user[0] == recipient :
            try:
                send_message_to_client(user[2], f"{address}~{recipient}~{message}")
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
    try:
     if isinstance(client, socket.socket):
        client.close()
     else:
        print(f"Client {client} không phải là đối tượng socket")
    except Exception as e: print(f"Lỗi khi đóng kết nối với client: {e}")

    # send_user_list()  # Update user list when a client disconnects

# Function to handle client connections
def client_handler(client,address):
    try:
        data = client.recv(2048).decode('utf-8')
        # user_id,user_name = client.recv(2048).decode('utf-8')
        if '~' in data:
            user_id, user_name=data.split('~')
            print(f"Client {user_id}:{user_name}")
            active_clients.append((user_id,user_name, client,address))
            # send_user_list()  # Send updated user list to everyone
            threading.Thread(target=listen_for_messages, args=(client, user_id,address)).start()
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
            threading.Thread(target=client_handler, args=(client,address)).start()
        except Exception as e:
            print(f"Error accepting connections: {e}")

if __name__ == '__main__':
    main()
