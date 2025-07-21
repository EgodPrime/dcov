package com.kb310.exampleput;


public class ExamplePUT {
    public void m1(){
        System.out.println("Hello I am public void m1");
    }

    private void m2(){
        System.out.println("Hello I am private void m2");
    }

    private void m3(int x){
        if(x>5){
            System.out.println("x is greater than 5");
        } else {
            System.out.println("x is not greater than 5");
        }
    }

    private void m4(int x){
        switch (x) {
            case 1:
                System.out.println("x is 1");
                break;
            case 2:
                System.out.println("x is 2");
                break;
            case 3:
                System.out.println("x is 3");
                break;
            default:
                break;
        }
    }

    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println("Hello I am an example PUT");
        ExamplePUT examplePUT = new ExamplePUT();
        System.out.println("=========================================");
        examplePUT.m1();
        System.out.println("=========================================");
        examplePUT.m2();
        System.out.println("=========================================");
        examplePUT.m3(10);
        System.out.println("=========================================");
        examplePUT.m3(3);
        System.out.println("=========================================");
        examplePUT.m4(1);
        System.out.println("=========================================");
        examplePUT.m4(2);
        System.out.println("=========================================");
        examplePUT.m4(3);
        System.out.println("=========================================");
        examplePUT.m4(4);
    }
}
