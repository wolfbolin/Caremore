package com.wolfbolin.caremore;

import android.annotation.SuppressLint;
import android.media.MediaPlayer;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.baidu.mapapi.SDKInitializer;
import com.baidu.mapapi.map.BaiduMap;
import com.baidu.mapapi.map.BitmapDescriptor;
import com.baidu.mapapi.map.BitmapDescriptorFactory;
import com.baidu.mapapi.map.MapStatus;
import com.baidu.mapapi.map.MapStatusUpdate;
import com.baidu.mapapi.map.MapStatusUpdateFactory;
import com.baidu.mapapi.map.MarkerOptions;
import com.baidu.mapapi.map.OverlayOptions;
import com.baidu.mapapi.map.TextureMapView;
import com.baidu.mapapi.model.LatLng;

import java.io.File;
import java.io.IOException;

public class ShowMessage extends AppCompatActivity {
    private TextView str_date;
    private TextView str_type;
    private TextView str_level;
    private TextView str_heart;
    private TextView str_message;
    private Button but_audio_network;
    private Button but_audio_local;

    private TextureMapView mMapView;
    private BaiduMap mBaiduMap;

    private String message_date;
    private String message_type;
    private String message_level;
    private String message_heart;
    private String message_message;
    private String message_lng;
    private String message_lat;
    private String message_audio;
    private String audio_url;

    MediaPlayer mMediaPlayer;

    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        SDKInitializer.initialize(getApplicationContext());
        setContentView(R.layout.activity_message);

        str_date = (TextView)findViewById(R.id.tv_date);
        str_type = (TextView)findViewById(R.id.tv_type);
        str_level = (TextView)findViewById(R.id.tv_level);
        str_heart = (TextView)findViewById(R.id.tv_heart);
        str_message = (TextView)findViewById(R.id.tv_message);
        but_audio_network = (Button) findViewById(R.id.bt_audio_network);
        but_audio_local = (Button) findViewById(R.id.bt_audio_local);
        mMapView = (TextureMapView) findViewById(R.id.mTexturemap);
        mBaiduMap = mMapView.getMap();

        message_date = getIntent().getStringExtra("date");
        message_type = getIntent().getStringExtra("type");
        message_level = getIntent().getStringExtra("level");
        message_heart = getIntent().getStringExtra("heart");
        message_message = getIntent().getStringExtra("message");
        message_lat = getIntent().getStringExtra("lat");
        message_lng = getIntent().getStringExtra("lng");
        message_audio = getIntent().getStringExtra("audio");
        audio_url = getIntent().getStringExtra("audio_url");

        str_date.setText(message_date.substring(0,4)+"年"
        +message_date.substring(4,6)+"月"
        +message_date.substring(6,8)+"日"
        +message_date.substring(8,10)+"时"
        +message_date.substring(10,12)+"分");
        str_type.setText(message_type);
        str_level.setText(message_level);
        str_heart.setText(message_heart);
        str_message.setText(message_message);

        LatLng point = new LatLng(Double.parseDouble(message_lat),Double.parseDouble(message_lng));
        BitmapDescriptor bitmap = BitmapDescriptorFactory
                .fromResource(R.drawable.icon_marka);
        OverlayOptions option = new MarkerOptions().position(point).icon(bitmap);
        mBaiduMap.addOverlay(option);
        final MapStatus mMapStatus = new MapStatus.Builder().target(point).zoom(17).build();
        MapStatusUpdate mMapStatusUpdate = MapStatusUpdateFactory.newMapStatus(mMapStatus);
        mBaiduMap.setMapStatus(mMapStatusUpdate);

        mMediaPlayer = new MediaPlayer();

        but_audio_network.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    mMediaPlayer.reset();
                    mMediaPlayer.setDataSource(audio_url+message_audio);
                    mMediaPlayer.prepareAsync();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
        but_audio_local.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    mMediaPlayer.reset();
                    mMediaPlayer.setDataSource(Environment.getExternalStorageDirectory()+ File.separator+message_audio);
                    mMediaPlayer.prepare();
                    mMediaPlayer.start();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }
}
