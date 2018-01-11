str = 'AT:'
str = str.split(':')
print(type(str))
print(len(str))
if len(str) != 2 or len(str[1]) == 0:
    print("error")
else:
    print("success")