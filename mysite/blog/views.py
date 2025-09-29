from django.shortcuts import render, get_object_or_404

from .form import EmailPostFrom
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status = Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month = month,
                             publish__day = day)
    return render(request, 'blog/post/detail.html', {'post': post})

class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):

    post = get_object_or_404(Post,
                             id = post_id,
                             status = Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} рекомендует почитать: {post.title}"

            message = (
                f"Прочитайте «{post.title}» здесь: {post_url}\n\n"
                f"Комментарий от {cd['name']}: {cd['comments']}"
            )
            send_mail(subject, message, 'gluhovvladislav514@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostFrom()
    return render(request, 'blog/post/share.html', {'post': post,
                                                                        'form': form,
                                                                         'sent': sent})