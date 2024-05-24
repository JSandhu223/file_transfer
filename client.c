#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>


int main(int argc, char** argv)
{
    // TODO: get hostname and port from command line
    char hostname[] = "localhost";
    uint16_t port = 8020; // 2 bytes (just to be safe)

    // Address info
    struct sockaddr_in server_addr;

    // Zero out the struct
    memset(&server_addr, 0, sizeof(server_addr));
    // Set family to IPv4
    server_addr.sin_family = AF_INET;
    // Set port number (in network byte order / big endian)
    server_addr.sin_port = htons(port);

    // DEBUG LINES
    printf("Family: %d\n", server_addr.sin_family);
    printf("Port: %d\n", server_addr.sin_port);

    return 0;
}