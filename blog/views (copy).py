from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .models import Post
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm

# Create your views here.

me = get_user_model().objects.get(username="emilien")

def post_list(request):
    post_form = PostForm()
    posts = Post.objects.all().order_by('-created_date')
    
    return render(request,'blog/post_list.html',locals())

@csrf_exempt
def add_record(request):
    if request.POST:
        title = request.POST['title']
        text = request.POST['text']
        newpost = Post.objects.create(author = me, title=title, text=text)
    return redirect('/blog')

def post_record(request,id):
    posts = Post.objects.filter(id__lte=id)[::-1][:2]
    post = posts[0]
    next_post = posts[1] if len(posts) > 1 else None
    return render(request, 'blog/post_record.html', locals())



