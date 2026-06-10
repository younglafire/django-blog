from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class PublishedManager(models.Manager): # Custom manager

    def get_queryset(self):
        return(
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

class Post(models.Model):
    class Status(models.TextChoices):
        # 'DF' is value and 'Draft' is labels, which is human-readable name
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
        )
    
    #ForeignKey is a column that points to another models primary key
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
        
        
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    
    objects = models.Manager() # The default manager
    published = PublishedManager() # Custom manager
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
            ]
    def __str__(self):
        return self.title
    
    def get_absolute_url(self): 
        return reverse(
            'blog:post_detail', # return the url in urls.py, then can be used globally
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )