from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForms
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User



User = get_user_model()

# Create your views here.
@require_http_methods(['GET', 'POST'])
def hulogin(request):
    if request.method == 'GET':
        return render(request, template_name='login.html')
    else:
        form = LoginForms(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()

            # 打印获取到的用户信息
            print(f"用户信息: email={email}, password={password}, remember={remember}")

            if user and user.check_password(password):
                # 用户认证成功
                print(f"用户 {email} 登录成功")  # 输出成功信息到终端


                login(request, user)
                # user.is_authenticated



                if not remember:
                    request.session.set_expiry(0)
                
                return redirect('/')  # 登录成功后重定向到主页
            else:
                # 用户认证失败
                print("邮箱或密码错误")  # 输出错误信息到终端
                form.add_error('email', 'The email address or password is incorrect')
                return render(request, template_name='login.html', context={"form": form})
        else:
            # 表单无效的情况
            print("表单无效：", form.errors)  # 输出表单错误信息到终端
            return render(request, template_name='login.html', context={"form": form})


def hulogout(request):
    logout(request)
    return redirect('/')

    

@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,template_name='register.html')

    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email,username=username,password=password)
            return redirect(reverse('author:login'))
        else:
            print(form.errors)
            #重新跳转到登录界面
            return redirect(reverse('author:register'))
            # return render(request,'register.html',context={"form":form})
        

def send_email_captcha(request):
    #?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code":400,"message":'The mailbox must be delivered!'})


    #生成验证码(取4位阿拉伯数字)
    #['0','2','9','8']
    captcha ="".join(random.sample(string.digits,k=4))
    # print(captcha)

    #存储到数据库
    CaptchaModel.objects.update_or_create(email = email,defaults={'captcha':captcha})
    send_mail("Jw Hub Captcha",message=f"Your registration verification code is:{ captcha}",recipient_list=[email],from_email=None)
    return JsonResponse({"code":200,"message": "The email verification code is successfully sent"})