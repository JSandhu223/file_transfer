import sys
import time
import socket
import platform # for determining client's OS


# Note: a string representation of a negative number should never be passed here.
# This is for error handling the hostname and the port number, which are strictly positive.
def cast_to_int(s: str):
    try:
        x = int(s)
        return x
    except ValueError:
        return -1


def valid_hostname(host: str):
    if host == 'localhost':
        return True
    split_host = host.split('.')
    if len(split_host) != 4:
        return False
    for octet in split_host:
        if cast_to_int(octet) == -1:
            return False
    return True


def parse_args():
    if len(sys.argv) != 3:
        print("USAGE: python3 client.py <HOST> <PORT>")
        exit()
    hostname = sys.argv[1]
    if not valid_hostname(hostname):
        print("Invalid hostname")
        exit()
    port = cast_to_int(sys.argv[2])
    if port == -1:
        print("Invalid port! Port must be an integer")
        exit()
    return hostname, port


def create_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock
    except socket.error:
        print("Error creating socket")
        exit()


def connect_to_server(sock: socket, host: str, port: int):
    try:
        print(f"Connecting to {host}@{port} ...")
        sock.connect((host, port))
        return 0
    except ConnectionError:
        return -1


def send_data(sock: socket, data: bytes):
    try:
        sock.send(data)
        return 0
    except ConnectionError:
        print("Connection error on send()")
        return None
    except TimeoutError:
        print("Timeout on send()")
        return None
    except BlockingIOError:
        print("BlockingIOError on send()")
        return None
    except OSError:
        print("Socket error on send()")
        return None


def recv_data(sock: socket):
    try:
        data = sock.recv(1024)
        return data
    except ConnectionError as e:
        print("Connection error on recv()", e)
        return None
    except TimeoutError as e:
        print("Timeout on recv()", e)
        return None
    except BlockingIOError as e:
        print("BlockingIOError on recv()", e)
        return None
    except OSError as e:
        print("Socket error on recv()")
        return None


def close_socket(sock: socket):
    sock.close()


def main():
    # Parse command line arguments
    host, port = parse_args()

    while True:
        # Create TCP socket
        sock = create_socket()

        # Reconnect to server every 5 seconds upon failure
        if connect_to_server(sock, host, port) == -1:
            close_socket(sock)
            time.sleep(5)
            continue
        print(f"Connected to {host}@{port}")

        # Send the client's OS to the server upon successful connection
        os_platform = platform.system()
        if send_data(sock, os_platform.encode()) == None:
            print(f"Disconnected from {host}@{port}")
            close_socket(sock)
            time.sleep(5)
            continue

        while True:
            inp = input(">")
            if send_data(sock, inp.encode()) == None:
                print(f"Disconnected from {host}@{port}")
                break
            inp = inp.split()
            if inp[0] == 'quit':
                print("Goodbye")
                close_socket(sock)
                exit()
            elif inp[0] == 'download':
                pass
            else:
                data = recv_data(sock)
                if data == None:
                    print(f"Disconnected from {host}@{port}")
                    break
                print(data.decode())


if __name__ == '__main__':
    main()