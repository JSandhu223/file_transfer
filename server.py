import sys
import socket
import platform # for determining host OS


def get_host_windows():
    hostname = socket.gethostname()
    # Usage: getaddrinfo(hostname, port)
    addr_info = socket.getaddrinfo(hostname, None)
    for s in addr_info:
        print(s)


# On WSL, the private IP address may not be returned.
# So, we will use system calls to obtain the private IP
def get_host_linux():
    print("Work in progress ...")


def main():
    os_platform = platform.system()
    host = ''
    if os_platform == 'Windows':
        host = get_host_windows()
    else:
        host = get_host_linux()


if __name__ == '__main__':
    main()