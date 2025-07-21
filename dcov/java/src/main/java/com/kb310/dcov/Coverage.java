package com.kb310.dcov;

import com.sun.jna.Library;
import com.sun.jna.Native;

public class Coverage{
    private static int previousIndex = 0;

    public interface DcovLib extends Library {
        DcovLib INSTANCE = Native.load("dcov_java", DcovLib.class);

        void set_bit(long x);
    }


    private static final int FNV_OFFSET_BASIS = 216613626;
    private static final int FNV_PRIME = 16777219;
    private static final int MOD = 1<<20;
    
    /**
     * 计算两个 int 值的哈希值
     *
     * @param a 第一个 int 值
     * @param b 第二个 int 值
     * @return 哈希值
     */
    public static long calculateHash(int a, int b) {
        long hash = FNV_OFFSET_BASIS;
        hash = hash ^ a;
        hash = hash * FNV_PRIME;
        hash = hash ^ b;
        return hash % MOD;
    }

    public static void onHit(int idx){
        // System.out.println("Hit at index: " + idx);
        long edgeIndex=calculateHash(previousIndex, idx);
        previousIndex = idx;
        // System.out.println("Hit edge " + edgeIndex);
        DcovLib.INSTANCE.set_bit(edgeIndex);
    }
}