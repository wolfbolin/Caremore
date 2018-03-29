package com.wolfbolin.caremore;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.SocketTimeoutException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {
    private EditText str_url;
    private TextView str_http_status;
    private TextView tv_info_status;
    private TextView str_data_status;
    private TextView str_sure_status;
    private Button but_check;
    private Button but_info;
    private Button but_refresh;
    private Button but_sure;
    private Button but_show;

    private Handler handler;
    private String http_url;
    private String file_url;
    private String message_date;
    private String message_type;
    private String message_level;
    private String message_heart;
    private String message_message;
    private String message_lng;
    private String message_lat;
    private String message_audio;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        str_url = (EditText) findViewById(R.id.tv_url);
        str_http_status = (TextView) findViewById(R.id.tv_url_status);
        tv_info_status = (TextView) findViewById(R.id.tv_info_status);
        str_data_status = (TextView) findViewById(R.id.tv_data);
        str_sure_status = (TextView) findViewById(R.id.tv_sure_status);
        but_check = (Button) findViewById(R.id.bt_check);
        but_info = (Button)findViewById(R.id.bt_info);
        but_refresh = (Button) findViewById(R.id.bt_refresh);
        but_sure = (Button) findViewById(R.id.bt_sure);
        but_show = (Button) findViewById(R.id.bt_show);

        but_check.setOnClickListener(new View.OnClickListener() {
            @Override
            @SuppressLint("HandlerLeak")
            public void onClick(View v) {
                handler = null;
                handler = new Handler() {
                    public void handleMessage(Message msg) {
                        super.handleMessage(msg);
                        Log.d("WB", "[INFO](main_thread)Http response:" + msg.obj);
                        str_http_status.setText((String)msg.obj);
                    }
                };
                httpGet(str_url.getText().toString(), "/status");
            }
        });
        but_info.setOnClickListener(new View.OnClickListener() {
            @Override
            @SuppressLint("HandlerLeak")
            public void onClick(View v) {
                handler = null;
                handler = new Handler() {
                    public void handleMessage(Message msg) {
                        super.handleMessage(msg);
                        Log.d("WB", "[INFO](main_thread)Http response:" + msg.obj);
                        try {
                            tv_info_status.setText((String)msg.obj);
                            JSONObject jsonObj = new JSONObject((String)msg.obj);
                            if(jsonObj.getString("Status").equals("Fail")){
                                return;
                            }
                            message_lat = jsonObj.getString("Lat");
                            message_lng = jsonObj.getString("Lng");
                            message_heart = jsonObj.getString("Heart");
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                };
                httpGet(str_url.getText().toString(), "/info");
            }
        });
        but_refresh.setOnClickListener(new View.OnClickListener() {
            @Override
            @SuppressLint("HandlerLeak")
            public void onClick(View v) {
                handler = null;
                handler = new Handler() {
                    @SuppressLint("SetTextI18n")
                    public void handleMessage(Message msg) {
                        super.handleMessage(msg);
                        if(msg.arg1 == 200){
                            str_data_status.setText(str_data_status.getText()+"\n文件下载成功");
                            return;
                        }else if(msg.arg1 == 400){
                            str_data_status.setText(str_data_status.getText()+"\n文件下载失败");
                            return;
                        }

                        Log.d("WB", "[INFO](main_thread)Http response:" + msg.obj);
                        try {
                            str_data_status.setText((String)msg.obj);
                            JSONObject jsonObj = new JSONObject((String)msg.obj);
                            if(jsonObj.getString("Status").equals("Fail")){
                                return;
                            }
                            httpGetGile(str_url.getText().toString(), "/download/", jsonObj.getString("File"));
                            message_audio = jsonObj.getString("File");
                            message_date = jsonObj.getString("ID");
                            message_type = jsonObj.getString("Type");
                            message_level = jsonObj.getString("Level");
                            message_message = jsonObj.getString("Message");
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                };
                httpGet(str_url.getText().toString(), "/refresh");
            }
        });
        but_sure.setOnClickListener(new View.OnClickListener() {
            @Override
            @SuppressLint("HandlerLeak")
            public void onClick(View v) {
                handler = null;
                handler = new Handler() {
                    public void handleMessage(Message msg) {
                        super.handleMessage(msg);
                        Log.d("WB", "[INFO](main_thread)Http response:" + msg.obj);
                        str_sure_status.setText((String)msg.obj);
                    }
                };
                httpGet(str_url.getText().toString(), "/confirm");
            }
        });
        but_show.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, ShowMessage.class);
                intent.putExtra("date",message_date);
                intent.putExtra("type",message_type);
                intent.putExtra("level",message_level);
                intent.putExtra("heart",message_heart);
                intent.putExtra("message",message_message);
                intent.putExtra("lat",message_lat);
                intent.putExtra("lng",message_lng);
                intent.putExtra("audio",message_audio);
                intent.putExtra("audio_url", str_url.getText().toString()+"/player/");
                startActivity(intent);
            }
        });
    }

    public void httpGet(String url_header, String url_path) {
        http_url = url_header+url_path;
        Thread httpThread = new http_get_thread();
        httpThread.start();
    }

    class http_get_thread extends Thread {
        public void run() {
            URL httpurl;
            HttpURLConnection urlConnection = null;
            BufferedReader stream_in = null;
            String stream_buffer = "";
            StringBuilder stream_message = new StringBuilder();

            try {
                httpurl = new URL(http_url);
                urlConnection = (HttpURLConnection) httpurl.openConnection();
                urlConnection.setConnectTimeout(1000);
                stream_in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                while ((stream_buffer = stream_in.readLine()) != null) {
                    stream_message.append(stream_buffer);
                }
            }catch (SocketTimeoutException ignored) {
                stream_message = new StringBuilder("{\"Status\": \"Fail\",\"Message\": \"server stop\"}");
            }catch (java.io.IOException e) {
                stream_message = new StringBuilder("{\"Status\": \"Fail\",\"Message\": \"server stop\"}");
                e.printStackTrace();
            }
            Message msg = Message.obtain();
            msg.obj=stream_message.toString();
            handler.sendMessage(msg);
            Log.d("WB", "[INFO](http_thread)Http response:" + msg.obj);
        }
    }

    public void httpGetGile(String url_header, String url_path,String filename) {
        http_url = url_header+url_path+filename;
        file_url = Environment.getExternalStorageDirectory()+File.separator+filename;
        Thread httpThread = new http_download_thread();
        httpThread.start();
    }

    class http_download_thread extends Thread {
        public void run() {
            URL httpurl = null;
            File file = null;
            Message msg = Message.obtain();
            HttpURLConnection urlConnection = null;
            InputStream stream_in = null;
            OutputStream stream_out = null;
            int stream_buffer = 0;
            byte buffer[] = new byte[4*1024];
            try {
                file = new File(file_url);
                if(file.exists()){
                    file.delete();
                }
                file.createNewFile();
                stream_out = new FileOutputStream(file);
                httpurl = new URL(http_url);
                urlConnection = (HttpURLConnection) httpurl.openConnection();
                urlConnection.setRequestProperty("Connection","close");
                urlConnection.setConnectTimeout(1000);
                stream_in = urlConnection.getInputStream();
                while ((stream_buffer=stream_in.read(buffer)) != -1) {
                    stream_out.write(buffer,0,stream_buffer);
                }
                stream_out.flush();
                stream_in.close();
                stream_out.close();
                urlConnection.disconnect();
                msg.arg1=200;
            }catch (java.io.IOException e) {
                msg.arg1=400;
                e.printStackTrace();
            }finally {
                handler.sendMessage(msg);
            }

        }
    }
}
