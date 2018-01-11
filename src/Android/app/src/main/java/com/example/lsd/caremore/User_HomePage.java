package com.example.lsd.caremore;

/**
 * Created by LSD on 2017-08-07 .
 */

import android.app.TabActivity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.drawable.AnimationDrawable;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.amap.api.maps2d.AMap;
import com.amap.api.maps2d.CameraUpdate;
import com.amap.api.maps2d.CameraUpdateFactory;
import com.amap.api.maps2d.MapView;
import com.amap.api.maps2d.UiSettings;
import com.amap.api.maps2d.model.BitmapDescriptorFactory;
import com.amap.api.maps2d.model.CameraPosition;
import com.amap.api.maps2d.model.LatLng;
import com.amap.api.maps2d.model.Marker;
import com.amap.api.maps2d.model.MarkerOptions;

import java.io.File;
import java.io.IOException;

public class User_HomePage extends TabActivity {
 //   MediaPlayer player;
    String fileName="";
    LinearLayout voice_box;
    LinearLayout info_box1;
    LinearLayout info_box2;
    LinearLayout handle;
    TextView homepage_type;
    ImageView voice;
    TextView no_inform;
    TextView homepage_heart;
    Button mark_safe;
    boolean voice_on;
    Button btn_call;
    private MapView mapView;
    private AMap aMap;
    private CameraUpdate cameraUpdate;
    networkChangeReceiver networkChangeReceiver;
    GPSChangeReceiver gpsChangeReceiver;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //自定义标题
        requestWindowFeature(Window.FEATURE_CUSTOM_TITLE);
        setContentView(R.layout.activity_homepage);

        Intent startIntent = new Intent(User_HomePage.this,MyService.class);
        startService(startIntent);
        //player = new MediaPlayer();
        voice_on = false;
        voice_box = (LinearLayout)findViewById(R.id.voice_box);
        voice = (ImageView) findViewById(R.id.voice);
        no_inform = (TextView)findViewById(R.id.no_inform);
        info_box1 = (LinearLayout)findViewById(R.id.info_box1);
        info_box2 = (LinearLayout)findViewById(R.id.info_box2);
        handle = (LinearLayout)findViewById(R.id.handle);
        btn_call = (Button)findViewById(R.id.btn_call);
        mark_safe = (Button)findViewById(R.id.mark_safe);
        mapView = (MapView) findViewById(R.id.map);
        mapView.onCreate(savedInstanceState);// 此方法必须要调用----勿忘
        homepage_type = (TextView)findViewById(R.id.homepage_type);
        homepage_heart = (TextView)findViewById(R.id.homepage_heart);
        initView(28.1421200000,112.9835440000);

        info_box1.setVisibility(View.GONE);
        info_box2.setVisibility(View.GONE);
        voice_box.setVisibility(View.GONE);
        handle.setVisibility(View.GONE);
        btn_call.setVisibility(View.GONE);
        homepage_heart.setVisibility(View.GONE);
        /*
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                no_inform.setVisibility(View.GONE);
                voice_box.setVisibility(View.VISIBLE);
            }
        });*/
        voice_box.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(voice_on == false){
                    voice.setImageResource(R.drawable.voice_anim);
                    AnimationDrawable animationDrawable = (AnimationDrawable) voice.getDrawable();
                    animationDrawable.start();
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            startMusic(User_HomePage.this);
                        }
                    }).start();
                    voice_on = true;

                }else{
                    //player.stop();
                    voice.setImageResource(R.drawable.voice3);
                    voice_on = false;
                }
            }
        });
        //设置标题为某个layout
        getWindow().setFeatureInt(Window.FEATURE_CUSTOM_TITLE, R.layout.titlebar);
        //界面tab切换
      /*  TabHost tabHost = getTabHost();
        TabSpec page1 = tabHost.newTabSpec("tab1")
                .setIndicator("紧急通知")
                .setContent(R.id.tab01);
        tabHost.addTab(page1);

        TabSpec page2 = tabHost.newTabSpec("tab2")
                .setIndicator("位置信息")
                .setContent(R.id.tab02);
        tabHost.addTab(page2);
*/
        //设置响应
        ImageView picture_settings=(ImageView)findViewById(R.id.picture_settings);
        picture_settings.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent();
                intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                intent.setClass(User_HomePage.this, User_Settings.class);
                startActivity(intent);
            }
        });

        btn_call.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String phoneNumber = "18774805630";
                Intent dialIntent =  new Intent(Intent.ACTION_DIAL, Uri.parse("tel:" + phoneNumber));//跳转到拨号界面，同时传递电话号码
                startActivity(dialIntent);
            }
        });

        mark_safe.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_HomePage.this,safe_choose.class);
                startActivity(intent);
            }
        });

        IntentFilter intentFilter=new IntentFilter();
        intentFilter.addAction("123");
        networkChangeReceiver=new networkChangeReceiver();
        registerReceiver(networkChangeReceiver, intentFilter);

        IntentFilter intentFilter1 = new IntentFilter();
        intentFilter1.addAction("666");
        gpsChangeReceiver = new GPSChangeReceiver();
        registerReceiver(gpsChangeReceiver,intentFilter1);

    }

    private void initView(double x,double y) {

        if (aMap == null) {
            aMap = mapView.getMap();
            UiSettings uiSettings = aMap.getUiSettings();
            // 通过UISettings.setZoomControlsEnabled(boolean)来设置缩放按钮是否能显示
            uiSettings.setZoomControlsEnabled(false);
            //可视化区域，将指定位置指定到屏幕中心位置
            cameraUpdate = CameraUpdateFactory
                    .newCameraPosition(new CameraPosition(new LatLng(x, y), 18, 0, 30));
            aMap.moveCamera(cameraUpdate);
            drawMarkers(x,y);//绘制小蓝气泡
        }
    }

    private void drawMarkers(double x,double y) {

        MarkerOptions markerOptions = new MarkerOptions();
        // 设置Marker的坐标，为我们点击地图的经纬度坐标
        markerOptions.position(new LatLng(x, y));
        // 设置Marker点击之后显示的标题
        markerOptions.title("位置");
        // 设置Marker的图标样式
        markerOptions.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE));
        // 设置Marker是否可以被拖拽，
        markerOptions.draggable(false);
        // 设置Marker的可见性
        markerOptions.visible(true);
        //将Marker添加到地图上去
        Marker marker = aMap.addMarker(markerOptions);
        marker.showInfoWindow();
    }

    @Override
    protected void onResume() {
        // TODO Auto-generated method stub
        super.onResume();
        mapView.onResume();
    }
    @Override
    protected void onPause() {
        // TODO Auto-generated method stub
        super.onPause();
        mapView.onPause();
    }
    @Override
    protected void onDestroy() {
        // TODO Auto-generated method stub
        super.onDestroy();
        mapView.onDestroy();
        unregisterReceiver(networkChangeReceiver);
    }

    public void MoveMap(double x,double y) {
        aMap.clear();
        UiSettings uiSettings = aMap.getUiSettings();
        // 通过UISettings.setZoomControlsEnabled(boolean)来设置缩放按钮是否能显示
        uiSettings.setZoomControlsEnabled(false);
        cameraUpdate = CameraUpdateFactory
                .newCameraPosition(new CameraPosition(new LatLng(x, y),18 , 0, 30));
        aMap.moveCamera(cameraUpdate);
        drawMarkers(x,y);//绘制小蓝气泡


    }

    class networkChangeReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            String type = intent.getStringExtra("type");
            String lat = intent.getStringExtra("lat");
            String lng = intent.getStringExtra("lng");
            int heart = intent.getIntExtra("heart",-1);
            fileName = intent.getStringExtra("fileName");
            Toast.makeText(User_HomePage.this,"成功",Toast.LENGTH_SHORT).show();
            MoveMap(Double.valueOf(lat),Double.valueOf(lng));
            String tp = tranType(type);
            if(tp!=""){
                homepage_type.setText(tp);
                homepage_heart.setText("心率："+String.valueOf(heart));
            }

            showPreference();
            //addNotificaction(User_HomePage.this);
        }
    }

    class GPSChangeReceiver extends BroadcastReceiver{
        public void onReceive(Context context, Intent intent) {
            String lat = intent.getStringExtra("lat");
            String lng = intent.getStringExtra("lng");
            Toast.makeText(User_HomePage.this,"成功2",Toast.LENGTH_SHORT).show();
            MoveMap(Double.valueOf(lat),Double.valueOf(lng));
        }
    }

    private void startMusic(Context context){
        MediaPlayer player = new MediaPlayer();
        File file = new File(context.getFilesDir().getAbsolutePath(),fileName);
        if(file.exists()){
            System.out.println("存在");
            String path = file.getAbsolutePath();
            try {
                //System.out.println(path);
                AudioManager audioManager = (AudioManager) context.getSystemService(Context.AUDIO_SERVICE);
                audioManager.setMode(AudioManager.MODE_NORMAL);
                audioManager.setSpeakerphoneOn(true);
                player.reset();
                player.setDataSource(path);
                player.prepare();
                player.start();
            } catch (IOException e) {

            }
        }
    }

    private void showPreference(){
        no_inform.post(new Runnable() {
            @Override
            public void run() {
                no_inform.setVisibility(View.GONE);
            }
        });

        voice_box.post(new Runnable() {
            @Override
            public void run() {
                voice_box.setVisibility(View.VISIBLE);
            }
        });

        info_box1.post(new Runnable() {
            @Override
            public void run() {
                info_box1.setVisibility(View.VISIBLE);
            }
        });

        info_box2.post(new Runnable() {
            @Override
            public void run() {
                info_box2.setVisibility(View.VISIBLE);
            }
        });

        btn_call.post(new Runnable() {
            @Override
            public void run() {
                btn_call.setVisibility(View.VISIBLE);
            }
        });

        handle.post(new Runnable() {
            @Override
            public void run() {
                handle.setVisibility(View.VISIBLE);
            }
        });
        homepage_heart.post(new Runnable() {
            @Override
            public void run() {
                homepage_heart.setVisibility(View.VISIBLE);
            }
        });
    }

    private String tranType(String typeId){
        String _type = "";
        if(typeId.equals("1")){
            _type = "诱导";
        }else if(typeId.equals("2")){
            _type = "威胁";
        }else if(typeId.equals("3")){
            _type = "暴力";
        }
        return _type;
    }
}