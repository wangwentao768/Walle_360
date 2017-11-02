import os
import subprocess
import time
import tkinter.messagebox as msg
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory


def choose_apk_file():
    path_ = askopenfilename(filetypes=[('apk', '*.apk')])
    apk_file_path.set(path_)


def choose_keystore_file():
    path_ = askopenfilename(filetypes=[('keystore', '*.keystore')])
    keystore_file_path.set(path_)


def choose_out_path():
    path_ = askdirectory()
    out_path.set(path_)


def base_dir_path():
    basedir = sys.executable
    last_dir = basedir.rfind("/")
    basedir = basedir[:last_dir]
    return basedir


def do_sign():
    apk_path = apk_path_input.get()
    keystore_path = keystore_path_input.get()
    keystore_pwd = sign_pwd_input.get()
    channel_name = channel_input.get()
    output_path = out_input.get()
    if apk_path.strip() == '':
        msg.showerror('缺少内容', 'apk路径不能为空~')
    elif keystore_path.strip() == '':
        msg.showerror('缺少内容', '签名路径不能为空~')
    elif keystore_pwd.strip() == '':
        msg.showerror('缺少内容', '签名密码不能为空~')
    elif channel_name.strip() == '':
        msg.showerror('缺少内容', '渠道名称不能为空~')
    elif output_path.strip() == '':
        msg.showerror('缺少内容', '输出路径不能为空~')
    elif not os.path.exists(apk_path):
        msg.showerror('错误', 'apk文件不存在')
    elif not os.path.exists(keystore_path):
        msg.showerror('错误', '签名文件不存在')
    else:
        temp_apk = output_path + '/zipalignApk.apk'
        if os.path.exists(temp_apk):
            os.remove(temp_apk)
        zip_c = base_dir_path() + r'/support/zipalign -v 4 %s %s' % (apk_path, temp_apk)
        zip_result = subprocess.call(zip_c, shell=True)
        if zip_result == 0:
            sign_c = base_dir_path() + r'/support/apksigner sign --ks %s --ks-pass pass:%s %s' % (
                keystore_path, keystore_pwd, temp_apk)
            sign_result = subprocess.call(sign_c, shell=True)
            if sign_result == 0:
                check_c = 'java -jar ' + base_dir_path() + r'/support/CheckAndroidV2Signature.jar ' + temp_apk
                check_result = subprocess.call(check_c, shell=True)
                if check_result == 0:
                    channel_c = 'java -jar ' + base_dir_path() + r'/support/walle-cli-all.jar put -c ' \
                                + channel_name + ' ' + temp_apk + ' ' \
                                + output_path + '/%s-%s.apk' % (
                        channel_name, str(time.time()))
                    channel_result = subprocess.call(channel_c, shell=True)
                    if channel_result == 0:
                        msg.showinfo('完成', '签名完成')
                    else:
                        msg.showerror('错误', '写入渠道失败--' + channel_result)
                else:
                    msg.showerror('错误', '检查签名失败--' + check_result)
            else:
                msg.showerror('错误', '签名失败--' + sign_result)
        else:
            msg.showerror('错误', '优化失败--' + zip_result)


root = Tk()
root.title('sign helper tool')
root.geometry('500x300')

apk_file_path = StringVar()
keystore_file_path = StringVar()
out_path = StringVar()

path_choose_box = Frame(root)

Label(path_choose_box, text='apk路径:').grid(row=0, column=0)
apk_path_input = Entry(path_choose_box, textvariable=apk_file_path, width=40)
apk_path_input.grid(row=0, column=1, pady=10)
Button(path_choose_box, text='选择', command=choose_apk_file).grid(row=0, column=2, padx=5)
path_choose_box.pack()

Label(path_choose_box, text='签名路径:').grid(row=1, column=0)
keystore_path_input = Entry(path_choose_box, textvariable=keystore_file_path, width=40)
keystore_path_input.grid(row=1, column=1, pady=10)
Button(path_choose_box, text='选择', command=choose_keystore_file).grid(row=1, column=2, padx=5)
path_choose_box.pack()

Label(path_choose_box, text='签名密码:').grid(row=2, column=0)
sign_pwd_input = Entry(path_choose_box, width=40)
sign_pwd_input.grid(row=2, column=1, pady=10)
path_choose_box.pack()

Label(path_choose_box, text='渠道名称:').grid(row=3, column=0)
channel_input = Entry(path_choose_box, width=40)
channel_input.grid(row=3, column=1, pady=10)
path_choose_box.pack()

Label(path_choose_box, text='输出路径:').grid(row=4, column=0)
out_input = Entry(path_choose_box, textvariable=out_path, width=40)
out_input.grid(row=4, column=1, pady=10)
Button(path_choose_box, text='选择', command=choose_out_path).grid(row=4, column=2, padx=5)
path_choose_box.pack()

Button(path_choose_box, text='开始签名', command=do_sign).grid(row=5, column=1, padx=5)
path_choose_box.pack()

root.mainloop()
