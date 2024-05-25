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
    char hostname[] = "localhost";
    uint16_t port = 8020; // 2 bytes (just to be safe)

    // This is the server struct that we will bind to
    struct sockaddr_in server_addr;
    // Zero out the struct
    memset(&server_addr, 0, sizeof(server_addr));
    // Set family to IPv4
    server_addr.sin_family = AF_INET;
    // Set port number (in network byte order / big endian)
    server_addr.sin_port = htons(port);
    // Set hostname (as a long)
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // loopback address for now

    // Create socket for listening
    int sock = socket(PF_INET, SOCK_STREAM, 0);
    if (sock == -1)
    {
        printf("Failed to create listening socket\n");
        exit(1);
    }
    printf("Listening socket created\n");

    // Bind socket to struct
    if (bind(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1)
    {
        printf("Failed to bind\n");
        exit(1);
    }
    printf("Bind successful\n");

    return 0;
}