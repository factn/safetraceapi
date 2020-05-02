package org.safetraceapi.app.mpc;

import android.os.Build;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;

import com.facebook.react.bridge.Arguments;
import com.facebook.react.bridge.Promise;
import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;
import com.facebook.react.bridge.ReadableArray;
import com.facebook.react.bridge.WritableArray;
import com.facebook.react.module.annotations.ReactModule;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import org.json.JSONArray;
import org.json.JSONObject;
import org.safetraceapi.app.mpc.model.Schema;
import org.safetraceapi.app.mpc.model.Share;

import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

@ReactModule(name = MPCModule.NAME)
public class MPCModule extends ReactContextBaseJavaModule {
  private static ReactApplicationContext reactApplicationContext;
  private final int NUM_OF_PARTS = 3;
  private final int POLYNOMIAL_ORDER = 2;
  private SecureRandom secureRandom = new SecureRandom();
  private Scheme scheme = new Scheme(secureRandom, NUM_OF_PARTS, POLYNOMIAL_ORDER);

  public static final String NAME = "MPCModule";

  public MPCModule(ReactApplicationContext context) {
    reactApplicationContext = context;
  }
  
  @NonNull
  @Override
  public String getName() {
    return "MPCModule";
  }

  @ReactMethod
  public void splitShares(String sequence, Promise promise) {
    try {
      byte[] secret = parseStringToByteArray(sequence);
      final Map<Integer, byte[]> parts = scheme.split(secret);
      ArrayList<int[]> shares = new ArrayList<>();

      for (Map.Entry<Integer, byte[]> entry : parts.entrySet()) {
        byte[] vals = entry.getValue();

        for (byte val : vals) {
          shares.add(new int[]{entry.getKey(), val & 0xff});
        }
      }

      Gson gsonBuilder = new GsonBuilder().setPrettyPrinting().create();
      String JSONObject = gsonBuilder.toJson(shares);

      promise.resolve(JSONObject);
    } catch (Exception ex) {
      Log.e(NAME, "Caught exception while splitting shares. " + ex.getLocalizedMessage());
    }
  }
  
  @RequiresApi(api = Build.VERSION_CODES.N)
  @ReactMethod
  public void joinShares(ReadableArray shares, Promise promise) {
    try {
      ArrayList<Object> arrayList = shares.toArrayList();
      Map<Integer, byte[]> sharesMap = new HashMap<>();
      int index = 1;
      
      for(Object item : arrayList) {
        Log.d(NAME, item + "");

        JSONObject itemArr = new JSONObject(item.toString());
        JSONArray itemShares = (JSONArray) itemArr.get("shares");
        Schema los = parseShare(index, itemShares);
        sharesMap.put(los.index, los.vals);
        
        index++;
      }

      final byte[] recovered = scheme.join(sharesMap);
      StringBuilder result = new StringBuilder();

      for (byte str: recovered) {
        result.append(str);
      }
      
      promise.resolve(result.toString());      
    } catch (Exception ex) {
      Log.e(NAME, "Caught exception while joining shares. " + ex.getLocalizedMessage());
    }
  }

  private byte[] parseStringToByteArray(String str) {
    int strLen = str.length();
    byte[] res = new byte[strLen];

    for (int i = 0; i < strLen; i++) {
      char c = str.charAt(i);

      if (c == '0') res[i] = 0;
      else if (c == '1') res[i] = 1;
    }

    return res;
  }

  private Schema parseShare(int index, JSONArray arr) throws Exception {
    byte ba[] = new byte[arr.length()];
    
    for(int i = 0; i < arr.length(); i++) {
      JSONArray token = (JSONArray) arr.get(i);
      ba[i] = new Integer((int) token.get(1)).byteValue();
    }
    
    return new Schema(index, ba);
  }
}
