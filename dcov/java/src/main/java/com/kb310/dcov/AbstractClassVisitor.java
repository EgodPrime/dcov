package com.kb310.dcov;

import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.Opcodes;

public class AbstractClassVisitor extends ClassVisitor implements Opcodes{
    protected boolean isInterface = false;
    protected String className;

    public AbstractClassVisitor(int api, ClassVisitor cv) {
        super(api, cv);
    }
    
    @Override
    public void visit(int version, int access, String name, String signature, String superName, String[] interfaces) {
        cv.visit(version, access, name, signature, superName, interfaces);
        isInterface = (access & Opcodes.ACC_INTERFACE) != 0;
        this.className = name;
    }
}
