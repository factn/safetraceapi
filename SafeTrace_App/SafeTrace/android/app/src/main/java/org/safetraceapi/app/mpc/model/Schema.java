package org.safetraceapi.app.mpc.model;

public class Schema {
  public byte[] vals;
  public int index;

  public Schema(int i, byte[] _vals) {
    vals = _vals;
    index = i;
  }
}
