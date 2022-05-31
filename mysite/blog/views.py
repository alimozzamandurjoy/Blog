from django.shortcuts import get_object_or_404, render

from .models import *
from django.views.generic import ListView
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

# Create your views here.

def post_list(request,tag_slug=None):
    object_list= Post.objects.all()

    object= request.GET.get('search')
    if object != '' and object is not None:
        object_list= object_list.filter(title__icontains= object)
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug= tag_slug)
        object_list= object_list.filter(tags__in=[tag])
   
   
    paginator= Paginator(object_list,3)
    page= request.GET.get('page')
    try:
        posts= paginator.page(page)
    except PageNotAnInteger:
        posts= paginator.page(1)
    except EmptyPage:
        posts= paginator.page(paginator.num_pages)
    return render(request, 'blog/list.html',{'page':page,'posts':posts,'tag':tag})

def post_detail(request,year,month,day,post):
    post= get_object_or_404(Post,slug=post,status='published',publish__year= year,publish__month= month, publish__day= day)

    comments = post.comments.filter(active=True)

    new_comment= None
    if request.method== 'POST':
        comment_form = CommentForm(data= request.POST)
        if comment_form.is_valid():
            new_comment= comment_form.save(commit=False)
            new_comment.post= post
            new_comment.save()
    else:
        comment_form= CommentForm()

    return render(request,'blog/detail.html',{'post':post, 'comments':comments, 'new_comment': new_comment, 'comment_form': comment_form})



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
  
