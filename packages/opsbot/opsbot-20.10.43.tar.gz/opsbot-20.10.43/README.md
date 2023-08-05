# Opsbot-py 
Là một package python hỗ trợ việc Devops.
Được phân phối trên PyPi để các devops engineer có thể cài đặt thông qua lệnh 
```
pip install opsbot
```

## Build test local

```sh
pip install .
```

## Cấu hình lần đầu trước khi publish
Tạo file .pypirc trong thư mục $HOME với nội dung

```
[distutils]
index-servers =
    pypi

[pypi]
username: #go username tren he thong pypi.org
password: #go password tren he thong pypi.org
```

## Build & Publish lên PyPI
1. Chỉnh lại version trong file setup.py

2. Chạy lệnh build và upload
```sh
python setup.py sdist upload
```

3. Xem phiên bản mới đã publish tại
>https://pypi.org/project/opsbot/#history

4. Cài đặt lại một phiên bản cụ thể
```sh
pip install opsbot==x.x.x
```



## Usage
usage: opsbot.py [-h] {init,build} ...

I'm Opsbot. I can help you build the best devops scripts.

positional arguments:
  {init,build}  Avaiable commands
    init        Create .opsbot file, where you will write devops plan
    build       Build .opsbot file. export devops scripts

optional arguments:
  -h, --help    show this help message and exit