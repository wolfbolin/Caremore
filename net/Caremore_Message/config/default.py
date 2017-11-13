class Config(object):
    HOST = "127.0.0.1"
    PORT = 50009
    BUFSIZE = 10240000
    ENCODE = "utf8"
    DEBUG = False
    AVAILABLE_MESSAGE_TYPE = ["image", "file", "voice", "text"]
    DB = {
        'user': 'root',
        'password': 'root',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'mysql',
        'raise_on_warnings': True,
    }
