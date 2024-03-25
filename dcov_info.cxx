#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "dcov.h"

extern "C" int get_bitmap_size(){
    return bitmap_size;
}

extern "C" void open_bitmap_python(){
    shmid_python = shmget(shm_key_python, bytemap_size, IPC_CREAT | 0666);
    m_data_python = (unsigned char*) shmat(shmid_python, NULL, 0);
}

extern "C" void open_bitmap_c(){
    shmid_c = shmget(shm_key_c, bytemap_size, IPC_CREAT | 0666);
    m_data_c = (unsigned char*) shmat(shmid_c, NULL, 0);
}

extern "C" void open_bitmap(){
    open_bitmap_python();
    open_bitmap_c();
}

extern "C" void init_bitmap_python(){
    open_bitmap_python();
    memset(m_data_python, 0, bytemap_size);
}

extern "C" void init_bitmap_c(){
    open_bitmap_c();
    memset(m_data_c, 0, bytemap_size);
}

extern "C" void init_bitmap(){
    init_bitmap_python();
    init_bitmap_c();
}

extern "C" void clear_bitmap_python(){
    memset(m_data_python, 0, bytemap_size);
}

extern "C" void clear_bitmap_c(){
    memset(m_data_c, 0, bytemap_size);
}

extern "C" void clear_bitmap(){
    clear_bitmap_python();
    clear_bitmap_c();
}

extern "C" void randomize_bitmap_python(){
    for (size_t i = 0; i < bytemap_size; i++) {
        m_data_python[i] = rand() % 256;
    }
}

extern "C" void randomize_bitmap_c(){
    for (size_t i = 0; i < bytemap_size; i++) {
        m_data_c[i] = rand() % 256;
    }
}

extern "C" void randomize_bitmap(){
    for (size_t i = 0; i < bytemap_size; i++) {
        m_data_python[i] = rand() % 256;
        m_data_c[i] = rand() % 256;
    }
}

extern "C" void close_bitmap_python(){
    shmdt(m_data_python);
    shmctl(shmid_python, IPC_RMID, NULL);
}

extern "C" void close_bitmap_c(){
    shmdt(m_data_c);
    shmctl(shmid_c, IPC_RMID, NULL);
}

extern "C" void close_bitmap(){
    close_bitmap_python();
    close_bitmap_c();
}

unsigned int get_bb_cnt(unsigned char* m_data){
    unsigned int count = 0;
    #ifndef NO_PARALLEL 
        #pragma omp parallel for reduction(+:count)
    #endif
    for (size_t i = 0; i < bytemap_size; i++) {
        unsigned char c = m_data[i];
        #ifdef NORMAL_BIT_COUNT
            unsigned char byte = 1;
            for(size_t j=0;j<8;j++){
                if (c & byte) count ++;
                byte = byte << 1;
            }
        #else
            c = ( c & 0x55 ) + ( (c >> 1)  & 0x55 ) ;
            c = ( c & 0x33 ) + ( (c >> 2)  & 0x33 ) ;
            c = ( c & 0x0f ) + ( (c >> 4)  & 0x0f ) ;
            count += c;
        #endif
    }
    return count;
}

extern "C" unsigned int get_bb_cnt_python(){
    return get_bb_cnt(m_data_python);
}

extern "C" unsigned int get_bb_cnt_c(){
    return get_bb_cnt(m_data_c);
}

extern "C" void save_bitmap(){
    FILE* file_python = fopen("bitmap_python", "w");
    if (file_python == NULL) {
        perror("Error opening python bitmap");
        return;
    }
    FILE* file_c = fopen("bitmap_c", "w");
    if (file_c == NULL) {
        perror("Error opening c bitmap");
        return;
    }

    // 将内存中的数据写入文件
    size_t chunk_size = 1024;
    size_t elementsWritten = fwrite(m_data_python, chunk_size, bytemap_size/chunk_size, file_python);
    if (elementsWritten != bytemap_size) {
        perror("Error writing to python bitmap");
        fclose(file_python);
        return;
    }
    elementsWritten = fwrite(m_data_c, chunk_size, bytemap_size/chunk_size, file_c);
    if (elementsWritten != bytemap_size) {
        perror("Error writing to c bitmap");
        fclose(file_c);
        return;
    }

    // 关闭文件
    fclose(file_python);
    fclose(file_c);
}