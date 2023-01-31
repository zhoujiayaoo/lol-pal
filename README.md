## 太忙了没空整理，先开源，大家凑合着看
可以关注微信公众号《颜智科技》


### 依赖下载
```bash
# 没有用requirements.txt，用下面命令安装依赖
pip3 install pypiwin32 --trusted-host mirrors.aliyun.com
pip3 install opencv-python  --trusted-host mirrors.aliyun.com
pip3 install pillow --trusted-host mirrors.aliyun.com
pip3 install airtest --trusted-host mirrors.aliyun.com
pip3 install PyQt5 --trusted-host mirrors.aliyun.com
```


1队蓝队, 左边
2队红队, 右边



## 常见问题解决
```bash
# 无法加载文件 U:\lol-pal\venv\Scripts\activate.ps1，因为在此系统上禁止运行脚本。
```
解决
```bash
# 使用管理员打开 PowerShell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
