from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from grammar.utils import get_user_form_jwt


class BlogView(CreateView):
    template_name = 'blogs.html'
    form_class = PostForm
    permission_classes = [IsAuthenticated]  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Post.objects.all()
        context['comments'] = Comment.objects.all()
        context['formcomment'] = CommentForm

        if self.request.method == 'POST':
            formcom = CommentForm(data=self.request.POST)
            if formcom.is_valid():
                formcom.save()

        return context

    def form_invalid(self, form):
        messages.add_message(self.request, messages.SUCCESS, _("Uğurla göndərildi!"))
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        # JWT tokenindən istifadəçi məlumatlarını əldə et
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            messages.add_message(request, messages.ERROR, _("Autentifikasiya başlığı tapılmadı"))
            return redirect('login')

        token = auth_header.split(' ')[1]
        user_data = get_user_form_jwt(token)
        
        form = self.get_form()
        if form.is_valid():
            blog = form.save(commit=False)
            blog.userId_id = user_data['id']  
            blog.save()
            return redirect(reverse_lazy('blog'))

        return self.form_invalid(form)