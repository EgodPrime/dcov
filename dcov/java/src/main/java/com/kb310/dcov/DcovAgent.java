package com.kb310.dcov;

import java.lang.instrument.Instrumentation;

public class DcovAgent {
  public static void premain(String args, Instrumentation inst) {
    System.out.println("Start instrument ");
    String prefix = System.getenv("DCOV_JAVA_PREFIX");
    if(prefix == null){
        System.out.println("DCOV_JAVA_PREFIX is not set, dcov will use black list mode.");
    }
    inst.addTransformer(new DcovTransormer());
  }
}