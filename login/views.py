from django.shortcuts import render, redirect
from login import models
import hashlib


# Create your views here.

# 访问首页
def index(request):
    pass
    return render(request, 'login/index.html')


# 点击登录
def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')  # 获取不到时默认为空字符串
        password = request.POST.get('password', '')
        message = "所有字段必须填写！"
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(username=username) #匹配不到会报异常Exception: User matching query does not exist.
                MD5 = hashlib.md5() #创建MD5对象
                MD5.update(password.encode("utf-8"))    #将一个二进制数据进行md5处理，生成一个128位的二进制数据
                if user.password == MD5.hexdigest():    #将二进制结果转换成 十六进制的结果，4位二进制转换成1位十六进制
                    request.session['is_login']=True
                    request.session['user_id']=user.id
                    request.session['user_name'] = user.username
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except Exception as err:
                print('Exception:',err) #捕捉异常，并在控制台输出异常信息
                message = "用户名不存在"
        return render(request, 'login/login.html', locals())#local()返回当前所有的本地变量字典包含message和session中字段
    return render(request, 'login/login.html',locals())


# 点击注册
def register(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username','')
            password1 = request.POST.get('password1','')
            password2 = request.POST.get('password2','')
            email = request.POST.get('email')
            sex = request.POST.get('sex')
            message = "所有字段必须填写！"
            if username and password1 and password2 and email and sex:  #校验必填
                if password1 != password2:  # 判断两次密码是否相同
                    message = "两次输入的密码不一致！"
                    return render(request, 'login/register.html', locals())
                else:
                    same_name_user = models.User.objects.filter(username=username)
                    if same_name_user:  # 用户名唯一
                        message = '用户已经存在，请重新选择用户名！'
                        return render(request, 'login/register.html', locals())
                    same_email_user = models.User.objects.filter(email=email)
                    if same_email_user:  # 邮箱地址唯一
                        message = '该邮箱地址已被注册，请使用别的邮箱！'
                        return render(request, 'login/register.html', locals())

                    # 当一切都OK的情况下，创建新用户
                    new_user = models.User.objects.create()
                    new_user.username = username
                    MD5 = hashlib.md5()
                    MD5.update(password1.encode("utf-8"))
                    new_user.password = MD5.hexdigest()  # 使用加密密码
                    #new_user.password = password1
                    new_user.email = email
                    new_user.sex = sex
                    new_user.save()
                    message_assert = "注册成功！"
                    #return redirect('/login/')  # 自动跳转到登录页面
                    return render(request,'login/login.html',{"message_assert":message_assert})
            else:
                return render(request, 'login/register.html', locals())
    except Exception as e:
        print("Exception:",e)
    return render(request, 'login/register.html', locals())


# 点击退出
def logout(request):
    request.session.flush()
    return redirect('/index/')
