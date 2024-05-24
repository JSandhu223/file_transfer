#include <stdio.h>
#include <string.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>


int main(int argc, char** argv)
{
    char message[] = "hello";
    printf("%s\n", message);

    // Address info
    struct sockaddr_in server_addr;

    // Zero out the struct
    memset(&server_addr, 0, sizeof(server_addr));
    printf("Family: %d\n", server_addr.sin_family);
    printf("Port: %d\n", server_addr.sin_port);

    return 0;
}