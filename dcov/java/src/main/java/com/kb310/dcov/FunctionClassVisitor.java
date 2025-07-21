package com.kb310.dcov;

import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;

public class FunctionClassVisitor extends AbstractClassVisitor{
    private boolean isInterface = false;
    private String className;

    public FunctionClassVisitor(int api, ClassVisitor cv) {
        super(api, cv);
    }
    
    @Override
    public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
        MethodVisitor mv = super.visitMethod(access, name, desc, signature, exceptions);
        if(!isInterface && mv!=null && !"<init>".equals(name) && !"<clinit>".equals(name)){
            return new MethodVisitorAdapter(ASM9, mv, className, name);
        }
        return mv;
    }

    private class MethodVisitorAdapter extends MethodVisitor implements Opcodes{
        private String className = "";
        private String methodName = "";
        public MethodVisitorAdapter(int api, MethodVisitor mv, String className, String methodName) {
            super(api, mv);
            this.className = className;
            this.methodName = methodName;
        }
    
        @Override
        public void visitCode(){
            super.visitCode();
            // System.out.println(String.format("Insert method %s.%s with %d", className, methodName, DcovTransormer.cnt));
            visitLdcInsn(DcovTransormer.cnt);
            visitMethodInsn(Opcodes.INVOKESTATIC, "com/kb310/dcov/Coverage", "onHit", "(I)V", false);
            DcovTransormer.cnt++;
        }
    }
}
