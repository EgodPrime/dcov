#include <stdio.h>
#include <stdlib.h>

void x(int x){
    if (x == 0) {
        printf("x is 0\n");
    } else {
        printf("x is not 0\n");
    }
}

void y(int y){
    if (y < 0) {
        printf("y is negative\n");
    } else if (y==0){
        printf("y is 0\n");
    } else {
        printf("y is positive\n");
    }
}


void hello_world()
{
    printf("Hello World!\n");
}

int main(int argc, char *argv[])
{
    hello_world();
    x(atoi(argv[1]));
    y(atoi(argv[1]));
    return 0;
    
}