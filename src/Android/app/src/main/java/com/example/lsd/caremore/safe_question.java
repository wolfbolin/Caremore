package com.example.lsd.caremore;
//SplashActivity.java

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

public class safe_question extends AppCompatActivity {
    private Button next;
   // private Button pre;
    private LinearLayout l1;
    private LinearLayout l2;
    private LinearLayout l3;
    private LinearLayout l4;
    private TextView t1;
    private TextView t2;
    private TextView t3;
    private TextView t4;
    private int page;
    private boolean b1;
    private boolean b2;
    private boolean b3;
    private boolean b4;
    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
//        NO Title
      //  requestWindowFeature(Window.FEATURE_NO_TITLE);
      //  getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_safe_question);
        next = (Button)findViewById(R.id.question_next);
       // pre = (Button)findViewById(R.id.question_pre);
        l1 = (LinearLayout)findViewById(R.id.question_l1);
        l2 = (LinearLayout)findViewById(R.id.question_l2);
        l3 = (LinearLayout)findViewById(R.id.question_l3);
        l4 = (LinearLayout)findViewById(R.id.question_l4);
        t1 = (TextView)findViewById(R.id.question_t1);
        t2 = (TextView)findViewById(R.id.question_t2);
        t3 = (TextView)findViewById(R.id.question_t3);
        t4 = (TextView)findViewById(R.id.question_t4);
        page = 1;
        b1 = false;
        b2 = false;
        b3 = false;
        b4 = false;
        t1.setText("你要是敢说出去，我就打死你");
        t2.setText("我带你去一个地方然后买玩具给你好不好");
        t3.setText("你如果告诉你爸妈，他们就会不喜欢你，不要你了");
        t4.setText("你爸妈没空，让我来接你回家");
        l1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(b1 == false){
                    l1.setBackgroundColor(getResources().getColor(R.color.green));
                    b1 = true;
                }else{
                    l1.setBackgroundColor(getResources().getColor(R.color.white));
                    b1 = false;
                }
            }
        });
        l2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(b2 == false){
                    l2.setBackgroundColor(getResources().getColor(R.color.green));
                    b2 = true;
                }else{
                    l2.setBackgroundColor(getResources().getColor(R.color.white));
                    b2 = false;
                }
            }
        });
        l3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(b3 == false){
                    l3.setBackgroundColor(getResources().getColor(R.color.green));
                    b3 = true;
                }else{
                    l3.setBackgroundColor(getResources().getColor(R.color.white));
                    b3 = false;
                }
            }
        });
        l4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(b4 == false){
                    l4.setBackgroundColor(getResources().getColor(R.color.green));
                    b4 = true;
                }else{
                    l4.setBackgroundColor(getResources().getColor(R.color.white));
                    b4 = false;
                }
            }
        });
        next.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                page++;
                updateText(page);
            }
        });
/*
        pre.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(page > 1){
                    page--;
                    updateText(page);
                }
            }
        });
        */
    }

    private void updateText(int num){
        l1.setBackgroundColor(Color.parseColor("#ffffff"));
        l2.setBackgroundColor(Color.parseColor("#ffffff"));
        l3.setBackgroundColor(Color.parseColor("#ffffff"));
        l4.setBackgroundColor(Color.parseColor("#ffffff"));
        switch (num){
            case 1:
                t1.setText("你要是敢说出去，我就打死你");
                t2.setText("我带你去一个地方然后买玩具给你好不好");
                t3.setText("你如果告诉你爸妈，他们就会不喜欢你，不要你了");
                t4.setText("你爸妈没空，让我来接你回家");
                break;
            case 2:
                t1.setText("这件事你不要告诉你妈妈，不然你爸爸妈妈会不让你出来玩的");
                t2.setText("小伙子，请问户部巷在哪里啊，你能不能上车带我去啊，等回来了我给你买糖吃");
                t3.setText("这件事你要是敢说出去，你爸爸妈妈以后就不让你出来玩了");
                t4.setText("这件事如果被别人知道，你试试看");
                break;
            case 3:
                t1.setText("你过来我给你讲点事");
                t2.setText("我带你去一个地方然后买玩具给你好不好");
                t3.setText("你爸爸本来要来接你的，可是路上堵车了，跟我先上车吧");
                t4.setText("小朋友，你今年几年级了，在哪个学校啊？");
                break;
            case 4:
                Intent intent = new Intent(safe_question.this,User_HomePage.class);
                startActivity(intent);
            default:
                break;
        }
    }
}