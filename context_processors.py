from django.db.models import Count, Q
from blog.models import Category, Tag, Post

def common(request):
	context = {
	'categories': Category.objects.annotate(
		num_posts = Count('post', filter=Q(post__is_public=True))
		),
	'tags' : Tag.objects.annotate(
		num_posts=Count('post', filter=Q(post__is_public=True))
	).order_by("-num_posts"),
	'posts': Post.objects.filter(is_public=True).order_by("-published_at")
	}
	return context