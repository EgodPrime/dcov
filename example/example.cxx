#include <stdio.h>

extern "C" void test_switch(int a, int b){
    if (a){
        switch(b){
            case 1:
                printf("1");
                break;
            case 2:
                printf("2");
                break;
            case 3:
                printf("3");
                break;
            default:
                printf("default");
                break;
        }
    }else{
        switch(b){
            case 1:
                printf("a");
                break;
            case 2:
                printf("b");
                break;
            case 3:
                printf("c");
                break;
            default:
                printf("d");
                break;
        }
    }
}