# Caremore服务器使用接口规范

## 数据格式

每次数据传输都应包含三或四个连续的二进制段

> 4Bytes	#表示Json数据占用的字节长
>
> 4Bytes	#表示文件数据占用的字节长
>
> nBytes	#n字节的Json数据
>
> mBytes	#m字节的文件数据（如果有）

## json格式

Json中包含以下字段

| 键       | 类型     | 值              | 类型     |
| ------- | ------ | -------------- | ------ |
| Action  | string | GPS/Danger     | string |
| ID      | string | 20171123142236 | string |
| From    | string | Phone/IOT      | string |
| Lat     | string | 28.000000      | long   |
| Heart   | string | 60             | long   |
| Type    | string | 诱导/威胁/暴力       | string |
| Level   | string | 5              | long   |
| Message | string | 文本             | string |
| File    | string | xxxxx.wav      | string |

## 数据说明

* 以下字段不可为空

> Action
>
> From

* 有文件就一定需要文件名，即以下字段不可为空

> File

* 约定若某项数据不存在，在该键值对不存在于字典json中。即不可出现键对应空的值。