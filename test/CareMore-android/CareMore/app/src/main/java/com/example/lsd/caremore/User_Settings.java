package com.example.lsd.caremore;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.view.View;
import android.widget.LinearLayout;

/**
 * Created by LSD on 2017-08-03 .
 */
public class User_Settings extends AppCompatActivity {
    private LinearLayout history;
    private LinearLayout setting_safe;
    private LinearLayout setting_about;
    private LinearLayout setting_IP;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        //设备绑定响应
        history = (LinearLayout)findViewById(R.id.history);
        history.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_Settings.this,HistoryActivity.class);
                startActivity(intent);
            }
        });
        LinearLayout DeviceBinding=(LinearLayout)findViewById(R.id.DeviceBinding);
        DeviceBinding.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent=new Intent();
                intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                intent.setClass(User_Settings.this,User_Device.class);
                startActivity(intent);
            }
        });
        setting_safe = (LinearLayout)findViewById(R.id.setting_safe);
        setting_safe.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_Settings.this,Setting_safe.class);
                startActivity(intent);
            }
        });

        setting_about = (LinearLayout)findViewById(R.id.setting_about);
        setting_about.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_Settings.this,AboutActivity.class);
                startActivity(intent);
            }
        });
        setting_IP = (LinearLayout)findViewById(R.id.setting_IP);
        setting_IP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_Settings.this,Setting_IP_activity.class);
                startActivity(intent);
            }
        });
        //返回
        android.support.v7.app.ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.setHomeButtonEnabled(true);
            actionBar.setDisplayHomeAsUpEnabled(true);
        }
    }
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                this.finish(); // back button
                return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
