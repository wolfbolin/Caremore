package com.example.lsd.caremore;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.Socket;
import java.net.URL;


public class ClientTest {
    public static String  IP_ADDR = "10.0.2.2";//服务器地址
    public static int PORT = 8000;//服务器端口号
    private DataInputStream dis;
    private FileOutputStream fos;
    private InputStream is;
    private String action;
    private String getLatLng;
    private String Lat = "";//28.1421200000
    private String Lng = "";//112.9835440000
    private String type = "";
    private String fileName = "";
    private int heart = -1;
    private Context context;
    private Socket socket = null;

    public ClientTest(Context context) {
        super();
        this.context = context;

    }

    public void run() {
        new Thread(new Runnable(){

            @Override
            public void run() {
                String _ip="";
                int _port = -1;
                DatabaseHelper _dbHelper3 = new DatabaseHelper(context, "test1");
                SQLiteDatabase _db3 = _dbHelper3.getWritableDatabase();
                //创建游标对象
                Cursor cursor = _db3.query("history",new String[]{"id","filename","hrate"},"id=?", new String[]{"255"}, null, null, null,null);
                //利用游标遍历所有数据对象
                while(cursor.moveToNext()){
                    _ip  = cursor.getString(cursor.getColumnIndex("filename"));
                    _port = cursor.getInt(cursor.getColumnIndex("hrate"));
                }
                if(!_ip.equals("")&&_port!=-1){
                    IP_ADDR = _ip;
                    PORT = _port;
                }
                System.out.println(IP_ADDR+"  "+PORT);
                try {
                    //创建一个流套接字并将其连接到指定主机上的指定端口号
                    socket = new Socket(IP_ADDR, PORT);
                    is = socket.getInputStream();


                    byte[] msg = new byte[83886080];
                    int a =  is.read(msg);
                    System.out.print(a);
                    //String s = new String(msg,"UTF-8");
                    //System.out.print(s);
                    System.out.println("-------receive begin-------");
                    receiveMessage(msg);
                    //addNotificaction(context);
                    Intent intent = new Intent();
                    intent.putExtra("lat",Lat);
                    intent.putExtra("lng",Lng);
                    if(action.equals("GPS")){
                        System.out.println("这是gps");
                        intent.setAction("666");
                    }else if(action.equals("Danger")){
                        System.out.println("这是danger");
                        intent.setAction("123");
                        intent.putExtra("type",type);
                        intent.putExtra("fileName",fileName);
                        intent.putExtra("heart",heart);
                    }


                    context.sendBroadcast(intent);

                    Lat = "";
                    Lng = "";
                    System.out.println("-------receive end-------");

                } catch (Exception e) {
                    System.out.println("客户端run异常:" + e.getMessage());
                } finally {
                    if (socket != null) {
                        try {
                            socket.close();
                        } catch (IOException e) {
                            socket = null;
                            System.out.println("客户端 finally 异常:" + e.getMessage());
                        }
                    }
                    if(fos!=null){
                        try {
                            fos.close();
                        } catch (IOException e) {

                        }
                    }
                    if(is!=null){
                        try {
                            is.close();
                        } catch (IOException e) {

                        }
                    }
                }
            }

        }).start();
    }


    public void receiveMessage(byte[] msg) {
        byte[] len1 = new byte[4];
        System.arraycopy(msg, 0, len1, 0, 4);
        int contextLenth1 = getInt(len1);
        //System.out.print("*****"+contextLenth1+"*****");
        byte[] len2 = new byte[4];
        System.arraycopy(msg, 4, len2, 0, 4);
        int contextLenth2 = getInt(len2);

        byte[] context1 = new byte[contextLenth1];
        System.arraycopy(msg, 8, context1, 0, contextLenth1);

        byte[] context2 = new byte[contextLenth2];
        System.arraycopy(msg,8+contextLenth1,context2,0,contextLenth2);

        try {

            String jsonStr = new String(context1,"UTF-8");
            // System.out.print(jsonStr);
            JSONObject jsonObj = new JSONObject(jsonStr);
            action = jsonObj.getString("Action");
            System.out.println(action);
            String lat = jsonObj.getString("Lat");
            System.out.println(String.valueOf(lat));
            String lng = jsonObj.getString("Lng");
            System.out.println(String.valueOf(lng));
            getLatLng = "http://api.gpsspg.com/convert/coord/?oid=6570&key=FEC62F2D2C6A64E180CFE64F80653734&from=0&to=3&latlng="+ lat +","+lng;

            try {
                URL url = null;
                url = new URL(getLatLng);
                HttpURLConnection urlConnection = null;
                try {
                    urlConnection = (HttpURLConnection) url.openConnection();
                } catch (IOException e) {

                }
                BufferedReader in = null;
                try {
                    in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                } catch (IOException e) {

                }

                String lines="";
                String ss="";
                try {
                    while((lines = in.readLine()) != null){
                        ss+=lines;
                    }
                } catch (IOException e) {

                }
                JSONObject jso = new JSONObject(ss);
                JSONArray jsa = (JSONArray) jso.get("result");
                JSONObject jso2 = (JSONObject) jsa.get(0);
                Lat = jso2.getString("lat");
                Lng = jso2.getString("lng");
            } catch (MalformedURLException e) {

            }
            System.out.println("测试点1");
            if(action.equals("Danger")){
                System.out.println("测试点2");
                String from = jsonObj.getString("From");
                System.out.println(from);
                String id = jsonObj.getString("ID");
                System.out.println(id);

                type = jsonObj.getString("Type");
                System.out.println(type);
                long level = jsonObj.getLong("Level");
                System.out.println(String.valueOf(level));
                String message = jsonObj.getString("Message");
                System.out.println(message);
                heart = jsonObj.getInt("Heart");
                System.out.println(String.valueOf(heart));
                fileName = jsonObj.getString("File");
                System.out.println(fileName);
                //addNotificaction(context);

                //addNotificaction(context);



                if(!Lat.equals("")&&!Lng.equals("")){
                    System.out.println("测试点3");
                    DatabaseHelper dbHelper3 = new DatabaseHelper(context, "test1");
                    SQLiteDatabase db3 = dbHelper3.getWritableDatabase();

                    ContentValues values = new ContentValues();
                    values.put("id", id);
                    values.put("lon",Lat);
                    values.put("dim",Lng);
                    values.put("content",message);
                    values.put("filename",fileName);
                    values.put("hrate",heart);
                    values.put("grade",level);
                    values.put("type",type);

                    //数据库执行插入命令
                    db3.insert("history", null, values);

                }
                //addNotificaction(context);
                try {
                    save(fileName,context2);
                } catch (Exception e) {

                }

                addNotificaction(context);

            }

            //long id = jsonObj.getLong("ID");
        } catch (UnsupportedEncodingException e) {

        } catch (JSONException e) {

        }


    }
    public int getInt(byte[] bytes) {
        return (0xff & bytes[3]) | (0xff00 & (bytes[2] << 8)) | (0xff0000 & (bytes[1] << 16))
                | (0xff000000 & (bytes[0] << 24));
    }

    public void save(String filename, byte[] fileBytes) throws Exception {
        FileOutputStream outputStream = context.openFileOutput(filename, Context.MODE_PRIVATE);
        outputStream.write(fileBytes);
        outputStream.close();
    }

    public String read(String fileName) throws Exception {
        FileInputStream instream  = context.openFileInput(fileName);
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        int len = 0;
        while((len = instream.read(buffer)) != -1){
            outputStream.write(buffer,0,len);
        }
        byte []data = outputStream.toByteArray();
        return new String(data,"utf-8");
    }

    private void addNotificaction(Context t_context) {
        PendingIntent pendingIntent = PendingIntent.getActivity(t_context, 0,  new Intent(t_context, User_HomePage.class), 0);

        Notification notify= new Notification.Builder(t_context)
                .setSmallIcon(R.mipmap.ic_launcher) // 设置状态栏中的小图片，尺寸一般建议在24×24， 这里也可以设置大图标
                .setTicker("有新短消息了！")// 设置显示的提示文字
                .setContentTitle("危险")// 设置显示的标题
                .setContentText("您的孩子可能遇到危险！")// 消息的详细内容
                .setContentIntent(pendingIntent) // 关联PendingIntent
                .setNumber(1) // 在TextView的右方显示的数字，可以在外部定义一个变量，点击累加setNumber(count),这时显示的和
                .getNotification(); // 需要注意build()是在API level16及之后增加的，在API11中可以使用getNotificatin()来代替
        notify.flags |= Notification.FLAG_AUTO_CANCEL;
        NotificationManager manager =(NotificationManager) t_context.getSystemService(Context.NOTIFICATION_SERVICE);
        manager.notify(110, notify);

    }


}