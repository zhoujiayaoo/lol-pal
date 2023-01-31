pip3 install pypiwin32 --trusted-host mirrors.aliyun.com
pip3 install opencv-python  --trusted-host mirrors.aliyun.com
pip3 install pillow --trusted-host mirrors.aliyun.com
pip3 install airtest --trusted-host mirrors.aliyun.com
pip3 install PyQt5 --trusted-host mirrors.aliyun.com


1队蓝队, 左边
2队红队, 右边


# python程序打包成exe
pip3 install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/

## 常见问题解决
```bash
# 无法加载文件 U:\lol-pal\venv\Scripts\activate.ps1，因为在此系统上禁止运行脚本。
```
解决
```bash
# 使用管理员打开 PowerShell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
