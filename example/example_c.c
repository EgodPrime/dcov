#include <stdio.h>

void three_branches(int x){
   if(x == 1){
        printf("x = 1\n");
   }else if(x == 2){
        printf("x = 2\n");
   }else{
        printf("x = 3\n");
   }
}

int main(){
  three_branches(1);
  three_branches(2);
  three_branches(3);
  return 0;
}