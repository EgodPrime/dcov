package com.kb310.dcov;

import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.Label;

import java.util.ArrayList;

public class JumpLabelClassVisitor extends AbstractClassVisitor{
    
    protected static ArrayList<Label> jumpedLabels = new ArrayList<>();

    public JumpLabelClassVisitor(int api, ClassVisitor cv) {
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

    private class MethodVisitorAdapter extends MethodVisitor{
        private String className = "";
        private String methodName = "";

        public MethodVisitorAdapter(int api, MethodVisitor mv, String className, String methodName) {
            super(api, mv);
            this.className = className;
            this.methodName = methodName;
        }
    
        @Override
        public void visitJumpInsn(int opcode, Label label) {
            super.visitJumpInsn(opcode, label);
            jumpedLabels.add(label);
        }

        @Override
        public void visitLabel(Label label) {
            super.visitLabel(label);

            if(JumpLabelClassVisitor.jumpedLabels.contains(label)){
                System.out.println(String.format("Instrumenting on %s.%s.%s with %d ", className, methodName, label, DcovTransormer.cnt));
                visitLdcInsn(DcovTransormer.cnt);
                visitMethodInsn(Opcodes.INVOKESTATIC, "com/kb310/dcov/Coverage", "onHit", "(I)V", false);
                DcovTransormer.cnt++;
            }
        }

        @Override
        public void visitLookupSwitchInsn(Label dflt, int[] keys, Label[] labels) {
            super.visitLookupSwitchInsn(dflt, keys, labels);

            for(Label x: labels){
                jumpedLabels.add(x);
            }
        }

        @Override
        public void visitTableSwitchInsn(int min, int max, Label dflt, Label... labels) {
            super.visitTableSwitchInsn(min, max, dflt, labels);

            for(Label x: labels){
                jumpedLabels.add(x);
            }
        }

        @Override
        public void visitTryCatchBlock(Label start, Label end, Label handler, String type) {
            super.visitTryCatchBlock(start, end, handler, type);

            jumpedLabels.add(handler);
        }
    }

}

