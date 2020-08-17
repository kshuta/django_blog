from django.db import models
from django.db.models import Count
from django.utils import timezone
from markdownx.models import MarkdownxField
# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name




class Post(models.Model):
	category = models.ForeignKey(Category, on_delete=models.PROTECT)
	tags = models.ManyToManyField(Tag, blank=True)
	title = models.CharField(max_length=255)
	content = MarkdownxField('content', help_text="マークダウンで記述")
	description = models.TextField(blank=True)
	image = models.ImageField(
		upload_to='post_images/', null=True, blank=True
	)
	created_at = models.DateTimeField(auto_now_add=True)
	published_at = models.DateTimeField(blank=True, null=True)
	is_public = models.BooleanField(default=False)


	class Meta:
		ordering = ['-created_at']

	def save(self, *args, **kwargs):
		if self.is_public and not self.published_at:
			self.published_at = timezone.now()
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title






