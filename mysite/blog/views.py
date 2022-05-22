
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.views.generic import ListView
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request,'blog/list.html',{'posts':posts})

def post_detail(request,year,month,day,post):
    post= get_object_or_404(Post,slug=post,status='published',publish__year= year,publish__month= month, publish__day= day)
    return render(request,'blog/detail.html',{'post':post})

def post_list(request):
    object_list= Post.objects.all()
    paginator= Paginator(object_list,3)
    page= request.GET.get('page')
    try:
        posts= paginator.page(page)
    except PageNotAnInteger:
        posts= paginator.page(1)
    except EmptyPage:
        posts= paginator.page(paginator.num_pages)
    return render(request, 'blog/list.html',{'page':page,'posts':posts})

def post_share(request,post_id):
   post = get_object_or_404(Post, id= post_id, status= 'published')
   sent= False

   if request.method== 'POST':
       form = EmailPostForm(request.POST)
       if form.is_valid():
           cd = form.cleaned_data
           post_url = request.build_absolute_uri(
               post.get_absolute_url())

           subject = f"{cd['name']} recommends you read"\
                f"{post.title}"
           message = f"Read {post.title} at {post_url}\n\n"\
                f"{cd['name']}\'s comments: {cd['comments']}"
           send_mail(subject, message, 'alimozzamandurjoy2@gmail.com',[cd['to']])
           sent= True
   else:
       form= EmailPostForm()
   return render(request, 'blog/share.html',{'post':post,'form': form,'sent': sent})
  
