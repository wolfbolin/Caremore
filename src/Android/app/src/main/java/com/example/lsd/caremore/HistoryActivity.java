package com.example.lsd.caremore;

import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.List;

public class HistoryActivity extends AppCompatActivity {
    private ListView listview;
    private List<String> data = new ArrayList<String>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.history_layout);

 //       DatabaseHelper dbHelper6 = new DatabaseHelper(HistoryActivity.this,"test1");
  //      SQLiteDatabase db6 = dbHelper6.getReadableDatabase();

        //像ContentValues中存放数据
/*
   ContentValues values = new ContentValues();
        values.put("id", "201711021342360001");
        values.put("lon","28.1397780000");
        values.put("dim","112.9919820000");
        values.put("content","孩子，走吧");
        values.put("filename","c:/ad");
        values.put("hrate",100);
        values.put("grade",3);
        values.put("type","诱拐");
        DatabaseHelper dbHelper3 = new DatabaseHelper(HistoryActivity.this, "test");
        SQLiteDatabase db3 = dbHelper3.getWritableDatabase();
        //数据库执行插入命令
        db3.insert("record", null, values);

*/
/*
        DatabaseHelper dbHelper6 = new DatabaseHelper(HistoryActivity.this,"test");
        SQLiteDatabase db6 = dbHelper6.getWritableDatabase();
        db6.delete("record", "id=?", new String[]{"201711021342360001"});
        db6.execSQL("ALTER TABLE record ADD COLUMN type varchar(20)");
*/
        listview = (ListView) findViewById(R.id.listview);
        listview.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,getData()));
        listview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                String id = data.get(i);
                Intent intent = new Intent(HistoryActivity.this,HistoryItemActivity.class);
                intent.putExtra("history_id",id);
                startActivity(intent);

            }
        });
    }

    private List<String> getData(){
        DatabaseHelper dbHelper5 = new DatabaseHelper(HistoryActivity.this, "test1");
        SQLiteDatabase db5 = dbHelper5.getReadableDatabase();
        //创建游标对象
        Cursor cursor = db5.query("history",null,null, null, null, null, null);
        //利用游标遍历所有数据对象
        while(cursor.moveToNext()){
            String id = cursor.getString(cursor.getColumnIndex("id"));
            //日志打印输出
            if(!id.equals("255")){
                data.add(id);
            }
        }

        return data;
    }

}
