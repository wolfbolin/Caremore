package com.example.lsd.caremore;
//SplashActivity.java

import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.view.Window;
import android.view.WindowManager;

import com.amap.api.maps2d.AMap;
import com.amap.api.maps2d.CameraUpdate;
import com.amap.api.maps2d.CameraUpdateFactory;
import com.amap.api.maps2d.MapView;
import com.amap.api.maps2d.UiSettings;
import com.amap.api.maps2d.model.BitmapDescriptorFactory;
import com.amap.api.maps2d.model.CameraPosition;
import com.amap.api.maps2d.model.CircleOptions;
import com.amap.api.maps2d.model.LatLng;
import com.amap.api.maps2d.model.Marker;
import com.amap.api.maps2d.model.MarkerOptions;

public class Setting_safe extends AppCompatActivity implements AMap.OnMapClickListener {
    private Handler handler = new Handler();
    private MapView mapView;
    private AMap aMap;
    private CameraUpdate cameraUpdate;
    private int markerCounts;
    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
//        NO Title
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_setting_safe);
        mapView = (MapView) findViewById(R.id.safe_map);
        mapView.onCreate(savedInstanceState);// 此方法必须要调用----勿忘
        initView();

    }
    private void initView() {

        if (aMap == null) {
            aMap = mapView.getMap();
            UiSettings uiSettings = aMap.getUiSettings();
            // 通过UISettings.setZoomControlsEnabled(boolean)来设置缩放按钮是否能显示
            uiSettings.setZoomControlsEnabled(false);


            //可视化区域，将指定位置指定到屏幕中心位置
            cameraUpdate = CameraUpdateFactory
                    .newCameraPosition(new CameraPosition(new LatLng(28.1421200000,
                            112.9835440000), 18, 0, 30));
            aMap.moveCamera(cameraUpdate);
            aMap.setOnMapClickListener(this);
        }
    }

    private void drawMarkers() {

        MarkerOptions markerOptions = new MarkerOptions();
        // 设置Marker的坐标，为我们点击地图的经纬度坐标
        markerOptions.position(new LatLng(40.043212, 116.299728));
        // 设置Marker点击之后显示的标题
        markerOptions.title("八维");
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


    public void onMapClick(LatLng arg0) {
        aMap.clear();
        UiSettings uiSettings = aMap.getUiSettings();
        // 通过UISettings.setZoomControlsEnabled(boolean)来设置缩放按钮是否能显示
        uiSettings.setZoomControlsEnabled(false);
        MarkerOptions markerOptions = new MarkerOptions();
        markerOptions.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE));
        markerOptions.title("安全区域");
        markerOptions.position(arg0);

        aMap.addCircle(new CircleOptions().
                center(arg0).
                radius(150).
                fillColor(Color.argb(100, 0, 245,255 )).
                strokeColor(Color.argb(100, 0, 245, 255)).
                strokeWidth(15));
        markerOptions.visible(true);
        markerOptions.draggable(false);
        Marker marker = aMap.addMarker(markerOptions);
        marker.showInfoWindow();
    }
}
