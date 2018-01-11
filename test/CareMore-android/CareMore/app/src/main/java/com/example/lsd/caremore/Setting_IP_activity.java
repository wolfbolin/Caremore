package com.example.lsd.caremore;
//SplashActivity.java

import android.app.Activity;
import android.content.ContentValues;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class Setting_IP_activity extends Activity {
    private Button button;
    private String IP;
    private int PORT;
    private EditText IP_ip;
    private EditText IP_port;
    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
//        NO Title
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_setting_ip);
        button = (Button)findViewById(R.id.IP_change);
        IP_ip = (EditText)findViewById(R.id.IP_ip);
        IP_port = (EditText)findViewById(R.id.IP_port);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(IP_ip.getText().toString().equals("")||IP_port.getText().toString().equals("")){
                    Toast.makeText(Setting_IP_activity.this,"输入不能为空",Toast.LENGTH_SHORT).show();
                }else {
                    IP = IP_ip.getText().toString();
                    PORT = Integer.valueOf(IP_port.getText().toString());
                    DatabaseHelper dbHelper = new DatabaseHelper(Setting_IP_activity.this,"test1");
                    SQLiteDatabase db = dbHelper.getWritableDatabase();
                    db.delete("history","id=?",new String[]{"255"});
                    ContentValues values = new ContentValues();
                    //像ContentValues中存放数据
                    values.put("lon","");
                    values.put("dim","");
                    values.put("content","");
                    values.put("grade",-1);
                    values.put("type","");
                    values.put("id","255");
                    values.put("filename",IP);
                    values.put("hrate",PORT);
                    db.insert("history", null, values);
                    Toast.makeText(Setting_IP_activity.this,"修改成功",Toast.LENGTH_SHORT).show();
                }
            }
        });




    }
}