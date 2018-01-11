package com.example.lsd.caremore;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

import java.io.IOException;
import java.net.Socket;

public class MyService extends Service {

    public static final String TAG = "MyService";
    private Socket socket=null;
    ClientTest clientTest = new ClientTest(this);
    @Override
    public void onCreate() {
        super.onCreate();
        clientTest.run();
        Log.d(TAG, "onCreate() executed");

    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(TAG, "onStartCommand() executed");
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "onDestroy() executed");
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private void receiveMsg(){
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    socket = new Socket("10.0.2.2",8000);
                } catch (IOException e) {

                }
            }
        }).start();
    }


}
