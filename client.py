import sys
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
        sock.connect((host, port))
        print(f"Connected to {host}@{port}")
    except ConnectionError:
        print("Failed to connect to server")
        exit()


def close_socket(sock: socket):
    sock.close()


def main():
    # Parse command line arguments
    host, port = parse_args()
    # Create TCP socket
    sock = create_socket()
    connect_to_server(sock, host, port)

    # Also send the client's OS to the server
    os_platform = platform.system()

    while True:
        inp = input(">")
        sock.send(inp.encode())
        if inp == 'quit':
            print("Goodbye")
            break

    close_socket(sock)


if __name__ == '__main__':
    main()