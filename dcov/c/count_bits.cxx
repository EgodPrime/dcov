#include <stdio.h>
#include <sys/shm.h>
#include <stdlib.h>
#include "dcov_common.h"


uint32_t _count_bits(unsigned char* m_data){
    unsigned int count = 0;
    #pragma omp parallel for reduction(+:count)
    for (size_t i = 0; i < bytemap_size; i++) {
        unsigned char c = m_data[i];
        c = ( c & 0x55 ) + ( (c >> 1)  & 0x55 ) ;
        c = ( c & 0x33 ) + ( (c >> 2)  & 0x33 ) ;
        c = ( c & 0x0f ) + ( (c >> 4)  & 0x0f ) ;
        count += c;
    }
    return count;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <shm_key>\n", argv[0]);
        return 1;
    }

    int shm_key = atoi(argv[1]);
    int shmid = shmget(shm_key, bytemap_size, IPC_CREAT | 0666);
    void *m_data = shmat(shmid, NULL, 0);
    unsigned int count = _count_bits((unsigned char*)m_data);
    printf("%d bits have been hit\n", count);
    return 0;
}