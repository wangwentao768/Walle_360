# Walle_360
美团开源了批量打包神器Walle, 使用Walle打包之后，用360加固会出现渠道信息丢失的问题，这是一个解决这个问题的脚本

# 使用方法
1. 把用360加固过的apk放到originApk文件夹下，并重命名为originApk.apk
2. 把签名文件放到keystore中，并重命名为apk.keystore
3. 执行./jgSign.sh（如果提示权限不够，执行chmod +x ./jgSign.sh）
4. 输入签名密码
5. 输入要打入的渠道名

当提示渠道写入成功，生成的文件会放在finalDir中，已渠道名+时间命名

# 参考

https://github.com/Meituan-Dianping/walle

http://18e0c209.wiz01.com/share/s/0oUc890scQDx2tkMAj02NI0c3Ubmms31ckdr2UwE0E2X-bzY
