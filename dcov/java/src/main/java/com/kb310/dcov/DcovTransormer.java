package com.kb310.dcov;

import java.util.ArrayList;
import java.util.List;

import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.IllegalClassFormatException;
import java.security.ProtectionDomain;

import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Opcodes;


public class DcovTransormer implements ClassFileTransformer {
    protected static int cnt = 0;

    private static List<String> skipPrefixList = new ArrayList<String>(
        List.of(
            "java/",
            "javax/",
            "sun/reflect",
            "com/kb310",
            "jdk/",
            "sun/",
            "com/sun/"
        )
    );

    private static List<String> skipKeyword = new ArrayList<String> (
        List.of(
            "/internal/"
        )
    );

    private static List<String> classHasSeen = new ArrayList<String>();

    @Override
    public byte[] transform(
        ClassLoader loader, 
        String className, Class<?> classBeingRedefined,
        ProtectionDomain protectionDomain, 
        byte[] classfileBuffer) throws IllegalClassFormatException
    {
        if(classHasSeen.contains(className)){
            return classfileBuffer;
        }
        classHasSeen.add(className);

        String prefix = System.getenv("DCOV_JAVA_PREFIX");
        if(prefix==null){
            for(String sp : skipPrefixList){
                if(className.startsWith(sp)){
                    return classfileBuffer;
                }
            }
            for(String skw: skipKeyword){
                if(className.contains(skw)){
                    return classfileBuffer;
                }
            }
        }else{
            if(!className.startsWith(prefix)){
                return classfileBuffer;
            }
        }
 
        // System.out.println(String.format("Instrument %s", className));
        ClassReader classReader = new ClassReader(classfileBuffer);
        ClassWriter classWriter = new ClassWriter(classReader, ClassWriter.COMPUTE_FRAMES);
        classReader.accept(new FunctionClassVisitor(Opcodes.ASM9, classWriter), ClassReader.EXPAND_FRAMES);
        classReader = new ClassReader(classWriter.toByteArray());
        classWriter = new ClassWriter(classReader, ClassWriter.COMPUTE_FRAMES);
        classReader.accept(new JumpLabelClassVisitor(Opcodes.ASM9, classWriter), ClassReader.EXPAND_FRAMES);

        return classWriter.toByteArray();
    }
}
