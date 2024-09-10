from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request,template_name='index.html')

def blog_detail(request,blog_id):
    return render(request,template_name='blog_detail.html')


def pub_blog(request):
    return render(request,template_name='pub_blog.html')