import sys
import time
import socket
import platform # for determining server's OS
import os # for system calls
import subprocess # for system calls


def cast_port(s: str):
    try:
        x = int(s)
        # Port must be positive
        if x <= 0:
            return -1
        return x
    except ValueError:
        return -1


def parse_arg():
    if len(sys.argv) != 2:
        print("USAGE: python3 server.py <PORT>")
        exit()
    port = cast_port(sys.argv[1])
    if port == -1:
        print("Port must be a positive integer!")
        exit()
    return port


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


def list_dir(conn: socket, command: list[str]):
    ls_output = subprocess.check_output(command)
    send_data(conn, ls_output)


def send_cwd(conn: socket):
    current_dir = os.getcwd()
    # Send current directory to client
    if send_data(conn, current_dir.encode()) == None:
        print("Disconnected")
        return -1
    return 0


def transfer_file(conn: socket, file_name: str):
    try:
        file = open(f"in/{file_name}", 'rb')
        # Read the file
        chunk_size = 1024
        while True:
            # TODO: error handle read()
            chunk = file.read(chunk_size)
            # Check if EOF if reached
            if not chunk:
                eot = b'\x04'
                send_data(conn, eot)
                break
            time.sleep(1)
            send_data(conn, chunk)
        
        file.close()
    except OSError:
        print(f"Failed to open file '{file_name}'. Check file name!")


def main():
    os_platform = platform.system()
    # host = ''
    # if os_platform == 'Windows':
    #     host = get_host_windows()
    # else:
    #     host = get_host_linux()

    #############################################
    # For now, allow anyone to communicate
    host = '0.0.0.0'
    port = parse_arg()
    #############################################

    # Create socket and bind
    sock = create_socket()
    bind_socket(sock, host, port)

    while True:
        print("Listening for connection ...")
        listen_conn(sock)

        conn, addr = accept_conn(sock)

        # Receive client's OS information
        data = recv_data(conn)
        if data == None:
            continue
        client_os = data.decode()

        # Log client connection
        print(f"Connected: {addr} on {client_os}")

        # Poll client for commands
        while True:
            # Receive message from client
            data = recv_data(conn)
            if data == None:
                break
            message = data.decode()
            print(f"Received: {message}") # DEBUG LINE

            command = message.split()

            if command[0] == 'quit' or not message:
                break
            
            elif command[0] == 'ls':
                list_dir(conn, command)

            elif command[0] == 'pwd':
                send_cwd(conn)

            elif message[0] == 'download':
                file_name = message[1]
                transfer_file(conn, file_name)

            else:
                # If received command is invalid, ignore and continue polling client
                reponse = "Invalid command!"
                send_data(conn, reponse.encode())
                continue
        
        # This is printed whenever the inner loop breaks
        print(f"{addr[0]} disconnected")
    
    sock.close()


if __name__ == '__main__':
    main()