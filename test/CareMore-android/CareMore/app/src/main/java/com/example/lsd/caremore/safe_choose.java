package com.example.lsd.caremore;
//SplashActivity.java

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

public class safe_choose extends AppCompatActivity {
    private Button submit;
    private Button cancel;

    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
//        NO Title
      //  requestWindowFeature(Window.FEATURE_NO_TITLE);
      //  getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_safe_choos);
        submit = (Button)findViewById(R.id.safe_submit);
        cancel = (Button)findViewById(R.id.safe_cancel);
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(safe_choose.this,safe_notify.class);
                startActivity(intent);
            }
        });

        cancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent1 = new Intent(safe_choose.this,User_HomePage.class);
                startActivity(intent1);
            }
        });
    }
}