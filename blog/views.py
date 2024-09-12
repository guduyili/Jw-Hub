from django.shortcuts import render,redirect,reverse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST,require_GET
# Create your views here.
from .models import BlogCategory,Blog,BlogComment
from django.http.response import JsonResponse
from .forms import PubBlogForm
from django.db.models import Q

def index(request):
    blogs = Blog.objects.all()
    return render(request,template_name='index.html',context={"blogs":blogs})

def blog_detail(request,blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request,template_name='blog_detail.html',context={'blog':blog})


# @login_required(login_url=reverse_lazy("author:login"))
# @login_required(login_url=('/author/login'))


@require_http_methods(['GET', 'POST'])
@login_required()
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, template_name='pub_blog.html', context={"categories": categories})
    else:
        form = PubBlogForm(request.POST, request.FILES)  # 添加 request.FILES
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            img = form.cleaned_data.get('img')  # 确保表单能处理 img 字段
            blog = Blog.objects.create(
                title=title, 
                content=content, 
                category_id=category_id, 
                author=request.user, 
                img=img
            )
            return JsonResponse({"code": 200, "message": "The blog was successfully published!", "data": {"blog_id": blog.id}})
        else:
            print(form.errors)
            return JsonResponse({"code": 400, "message": "The parameter is incorrect!"})



@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content,blog_id=blog_id,author=request.user)
    #重新加载博客详情页
    return redirect(reverse("blog:blog_detail",kwargs={'blog_id':blog_id}))

@require_GET
def search(request):
    # 获取搜索关键字
    q = request.GET.get('q', '')  # 默认值为空字符串
    if q:
        # 在博客标题和内容中查找包含关键字的博客
        blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    else:
        blogs = Blog.objects.none()  # 如果搜索关键字为空，则返回空的 QuerySet
    return render(request, template_name='index.html', context={"blogs": blogs})



