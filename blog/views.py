from django.shortcuts import render
from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from blog.models import Post, Category, Tag, ContentImage


class PostDetailView(DetailView):
	model = Post 

	def get_object(self, queryset=None):
		obj = super().get_object(queryset=queryset)
		if not obj.is_public and not self.request.user.is_authenticated:
			raise Http404
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["photos"] = ContentImage.objects.filter(post=self.object.id)
		print(context["photos"])
		return context

class IndexView(ListView):
	model = Post 
	template_name = 'blog/index.html'

class CategoryListView(ListView):
	queryset = Category.objects.annotate(
		num_posts=Count('post', fliter=Q(post__is_public = True)))

class TagListView(ListView):
	queryset = Tag.objects.annotate(num_posts = Count('post', filter=Q(post__is_public=True))).order_by("-num_posts")


class CategoryPostView(ListView):
	model = Post
	template_name = 'blog/category_post.html'

	def get_queryset(self):
		category_slug = self.kwargs['category_slug']
		self.category = get_object_or_404(Category, slug=category_slug)
		qs = super().get_queryset().filter(category=self.category)
		return qs
	
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['category'] = self.category
		print(context)
		return context 

class TagPostView(ListView):
	model = Post
	template_name = 'blog/tag_post.html'

	def get_queryset(self):
		tag_slug = self.kwargs['tag_slug']
		self.tag = get_object_or_404(Tag, slug=tag_slug)
		qs = super().get_queryset().filter(tags=self.tag)
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tag'] = self.tag 
		print(context)
		return context


