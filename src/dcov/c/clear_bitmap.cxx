#include <stdio.h>
#include <sys/shm.h>
#include <stdlib.h>
#include <string.h>
#include "dcov_common.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <shm_key>\n", argv[0]);
        return 1;
    }

    int shm_key = atoi(argv[1]);
    int shmid = shmget(shm_key, bytemap_size, IPC_CREAT | 0666);
    void *m_data = shmat(shmid, NULL, 0);
    memset(m_data, 0, bytemap_size);
    printf("Bitmap %d has been cleared\n", shm_key);
    return 0;
}