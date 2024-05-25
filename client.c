#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
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

    // This structure contains the address information for which the client will connect to
    struct sockaddr_in server_addr;
    // Zero out the struct
    memset(&server_addr, 0, sizeof(server_addr));
    // Set family to IPv4
    server_addr.sin_family = AF_INET;
    // Set port number (in network byte order / big endian)
    server_addr.sin_port = htons(port);
    // Set hostname (as a long)
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // loopback address for now

    // DEBUG LINES
    printf("Family: %d\n", server_addr.sin_family);
    printf("Port: %d\n", server_addr.sin_port);

    // Create socket with arguments: IPv4, stream socket, TCP protocol
    int sock = socket(PF_INET, SOCK_STREAM, 0);
    if (sock == -1)
    {
        printf("Error creating socket\n");
    }
    printf("Socket created\n");

    // Connect to server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1)
    {
        printf("Failed to connect\n");
    }

    // Close socket
    close(sock);

    return 0;
}