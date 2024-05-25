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
    // Create socket for listening
    int sock = socket(PF_INET, SOCK_STREAM, 0);
    if (sock == -1)
    {
        printf("Failed to create listening socket\n");
        return 1;
    }
    printf("Listening socket created\n");

    return 0;
}