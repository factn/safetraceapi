package org.safetraceapi.app.mpc.model;

public class Share {
  public int x;
  public int y;

  public Share(int _x, int _y) {
    x = _x;
    y = _y & 0xff;
  }
}