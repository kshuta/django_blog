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
		return context

class IndexView(ListView):
	paginate_by = 10
	model = Post 
	template_name = 'blog/index.html'

class SearchPostView(ListView):
	paginate_by = 10
	model = Post
	template_name = "blog/search_post.html"

	def get_queryset(self):
		print("hello")
		query = self.request.GET.get('q')
		lookups = (
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(category__name__icontains=query) |
			Q(tags__name__icontains=query)
		)
		if query:
			qs = Post.objects.filter(lookups).distinct()
			return qs
		qs=super().get_queryset.filter()
		return qs

	def get_context_data(self, **kwargs):
		context=super().get_context_data(**kwargs)
		query = self.request.GET.get('q')
		context['query'] = query
		return context 

class CategoryListView(ListView):
	queryset = Category.objects.annotate(
		num_posts=Count('post', fliter=Q(post__is_public = True)))

class TagListView(ListView):
	queryset = Tag.objects.annotate(num_posts = Count('post', filter=Q(post__is_public=True))).order_by("-num_posts")


class CategoryPostView(ListView):
	paginate_by = 10
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
		return context 

class TagPostView(ListView):
	paginate_by = 10
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
		return context





