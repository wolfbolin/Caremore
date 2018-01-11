package com.example.lsd.caremore;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    private User user = new User();
    final int username=123;
    final String password="lsd";
    private EditText et_account;
    private EditText et_password;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        et_account = (EditText)findViewById(R.id.et_account);
        et_password = (EditText)findViewById(R.id.et_password);
        //注册响应
        TextView tv_register=(TextView)findViewById(R.id.tv_register);
        tv_register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent=new Intent();
                intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                intent.setClass(MainActivity.this,User_Register.class);
                startActivity(intent);
            }
        });
        //登录响应
        /*final EditText et_account = (EditText)findViewById(R.id.et_account);
        final String InputUsername = et_account.getText().toString();
        EditText et_password = (EditText)findViewById(R.id.et_password);
        final String InputPassword = et_password.getText().toString();*/
        Button bn_login=(Button)findViewById(R.id.bn_login);
        bn_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //if(InputUsername.equals(username) && InputPassword.equals(password)){
                if(et_password.getText().toString().equals("")||et_account.getText().toString().equals("")){
                    Toast.makeText(MainActivity.this,"账号或密码不能为空",Toast.LENGTH_SHORT).show();
                }else {
                    Intent intent=new Intent();
                    intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                    intent.setClass(MainActivity.this,safe_question.class);
                    startActivity(intent);
                }

                //}
                /*else {
                    Toast toast=Toast.makeText
                            (MainActivity.this,"账号或者密码错误",Toast.LENGTH_SHORT);
                    toast.show();
                }*/
            }
        });
    }
    public void register(View view){
        Intent intent = new Intent(this,User_Register.class);
        startActivity(intent);
    }
}
