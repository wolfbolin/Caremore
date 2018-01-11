package com.example.lsd.caremore;

import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.drawable.AnimationDrawable;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

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

public class HistoryItemActivity extends AppCompatActivity {
   // private MediaPlayer player;
    private String fileName;
    private boolean voice_on;
    private MapView mapView;
    private AMap aMap;
    private CameraUpdate cameraUpdate;
    private TextView history_hrate;
    private TextView history_grade;
    private TextView history_id;
    private TextView history_content;
    private TextView history_type;
    private LinearLayout history_voice_box;
    private ImageView history_voice;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.historyitem_layout);
     //   player = new MediaPlayer();
        history_id = (TextView)findViewById(R.id.history_id);
        history_grade = (TextView)findViewById(R.id.hisoty_grade);
        history_hrate = (TextView)findViewById(R.id.hisoty_hrate);
        history_content = (TextView)findViewById(R.id.history_content);
        history_type = (TextView)findViewById(R.id.hisoty_type);
        history_voice_box = (LinearLayout)findViewById(R.id.hisoty_voice_box);
        history_voice = (ImageView)findViewById(R.id.hisoty_voice);
        Intent intent = getIntent();
        if (intent!=null){
            String value = (String) intent.getExtras().get("history_id");
            String year = value.substring(0,4);
            String month = value.substring(4,6);
            String day = value.substring(6,8);
            String hour = value.substring(8,10);
            String min = value.substring(10,12);
            String sec = value.substring(12,14);
            double lon = Double.valueOf(getLon(value));
            double dim = Double.valueOf(getDim(value));
            history_id.setText(year+"年"+month+"月"+day+"日"+hour+"时"+min+"分"+sec+"秒");
            history_hrate.setText(String.valueOf(getHrate(value)));
            history_grade.setText(String.valueOf(getGrade(value)));
            history_content.setText(getContent(value));
            String tp = getType(value);
            String tp1 = tranType(tp);
            if(tp1!=""){
                history_type.setText(tp1);
            }
            mapView = (MapView) findViewById(R.id.history_map);
            mapView.onCreate(savedInstanceState);// 此方法必须要调用----勿忘
            fileName = getFilename(value);
            initView(getLat(value),getLng(value));

            history_voice_box.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    history_voice_box.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            if(voice_on == false){
                                history_voice.setImageResource(R.drawable.voice_anim);
                                AnimationDrawable animationDrawable = (AnimationDrawable) history_voice.getDrawable();
                                animationDrawable.start();
                                new Thread(new Runnable() {
                                    @Override
                                    public void run() {
                                        startMusic(HistoryItemActivity.this);
                                    }
                                }).start();
                                voice_on = true;

                            }else{
                        //        player.stop();
                                history_voice.setImageResource(R.drawable.voice3);
                                voice_on = false;
                            }
                        }
                    });
                }
            });
        }



    }

    private String getLon(String history_id){
        String lon="";
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryItemActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",new String[]{"id","lon"},"id=?",new String[]{history_id}, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            lon = cursor.getString(cursor.getColumnIndex("lon"));
        }
        return lon;
    }

    private String getDim(String history_id){
        String dim="";
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryItemActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",new String[]{"id","dim"},"id=?",new String[]{history_id}, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            dim = cursor.getString(cursor.getColumnIndex("dim"));
        }
        return dim;
    }

    private int getHrate(String history_id){
        int hrate = 0;
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryItemActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",new String[]{"id","hrate"},"id=?",new String[]{history_id}, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            hrate = cursor.getInt(cursor.getColumnIndex("hrate"));
        }
        return hrate;
    }

    private int getGrade(String history_id){
        int grade = 0;
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryItemActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",new String[]{"id","grade"},"id=?",new String[]{history_id}, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            grade = cursor.getInt(cursor.getColumnIndex("grade"));
        }
        return grade;
    }

    private String getFilename(String history_id){
        String filename="";
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryItemActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",new String[]{"id","filename"},"id=?",new String[]{history_id}, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            filename = cursor.getString(cursor.getColumnIndex("filename"));
        }
        return filename;
    }

    private String getContent(String history_id){
        String content="";
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryItemActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",new String[]{"id","content"},"id=?",new String[]{history_id}, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            content = cursor.getString(cursor.getColumnIndex("content"));
        }
        return content;
    }

    private String getType(String history_id){
        String type="";
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryItemActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",new String[]{"id","type"},"id=?",new String[]{history_id}, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            type = cursor.getString(cursor.getColumnIndex("type"));
        }
        return type;
    }

    private double getLat(String history_id){
        String lat = "";
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryItemActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",new String[]{"id","lon"},"id=?",new String[]{history_id}, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            lat = cursor.getString(cursor.getColumnIndex("lon"));
        }
        return Double.valueOf(lat);
    }

    private double getLng(String history_id){
        String lng = "";
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryItemActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",new String[]{"id","dim"},"id=?",new String[]{history_id}, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            lng = cursor.getString(cursor.getColumnIndex("dim"));
        }
        return Double.valueOf(lng);
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

    private void startMusic(Context context){
        MediaPlayer player = new MediaPlayer();
        File file = new File(context.getFilesDir().getAbsolutePath(),fileName);
        if(file.exists()){
            System.out.println("存在");
            String path = file.getAbsolutePath();
            try {
                player.setDataSource(path);
                player.prepare();
                player.start();
            } catch (IOException e) {

            }
        }
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
