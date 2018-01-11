package com.example.lsd.caremore;

/**
 * Created by 徐鹏 on 2017/8/3.
 */
public class User {
    private String userName;
    private String passWord;
    private String device_num;

    public String getPassWord() {
        return passWord;
    }

    public void setPassWord(String passWord) {
        this.passWord = passWord;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getDevice_num() {
        return device_num;
    }

    public void setDevice_num(String device_num) {
        this.device_num = device_num;
    }
}
