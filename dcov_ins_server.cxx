#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include<cstring>
#include<iostream>
using namespace std;

int main(){
    int shmid = shmget(4401, 4, IPC_CREAT | 0666);
    unsigned char* m_data = (unsigned char*) shmat(shmid, NULL, 0);
    memset(m_data, 0, 4);
    while(1){
        sleep(1);
        unsigned int bb_id = __atomic_load_4(m_data, __ATOMIC_SEQ_CST);
        cout<<"current bb_id = "<<bb_id<<endl;
    }
}