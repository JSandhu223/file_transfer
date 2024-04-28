import sys
import socket
import platform # for determining host OS


def get_host_windows():
    hostname = socket.gethostname()
    # Usage: getaddrinfo(hostname, port)
    addr_info = socket.getaddrinfo(hostname, None)
    for t in addr_info:
        print(t[4][0])


# On WSL, it may be case that getaddrinfo() does not return the private IP address.
# So, we will use system calls to obtain the private IP address.
def get_host_linux():
    print("Work in progress ...")


def create_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock
    except socket.error:
        print("Error creating socket")
        exit()


def bind_socket(sock: socket, host: str, port: int):
    try:
        sock.bind((host, port))
    except PermissionError as e:
        print("Permission error:", e)
        exit()
    except OSError as e:
        print("Error binding socket:", e)
        exit()


def listen_conn(sock: socket):
    try:
        sock.listen()
    except OSError as e:
        print("Error listening on socket:", e)
        exit()


def accept_conn(sock: socket):
    try:
        conn, addr = sock.accept()
        return conn, addr
    except OSError as e:
        print("Error accepting connection")
        exit()


def main():
    # os_platform = platform.system()
    # host = ''
    # if os_platform == 'Windows':
    #     host = get_host_windows()
    # else:
    #     host = get_host_linux()
    #############################################
    # For now, allow anyone to communicate
    host = '0.0.0.0'
    port = 8010
    #############################################

    # Create socket and bind
    sock = create_socket()
    bind_socket(sock, host, port)

    while True:
        print("Listening for connection ...")
        listen_conn(sock)

        conn, addr = accept_conn(sock)
        print(f"Connected: {addr}")

        # Receive message from client
        data = conn.recv(1024)
        message = data.decode()

        if message == 'q!':
            break

        print(message)
    
    sock.close()


if __name__ == '__main__':
    main()