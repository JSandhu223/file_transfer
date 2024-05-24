#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>


int main(int argc, char** argv)
{
    char message[] = "hello";
    printf("%s\n", message);

    return 0;
}