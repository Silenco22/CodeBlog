from django.db import models

from django.db.models.signals import post_delete, pre_save
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
import datetime


#funkcija vraca file path na koji se spremaju slike
def upload_location(instance, filename):
    file_path = 'images/blog/{author_id}/{title}-{filename}'.format(
        author_id = str(instance.author.id), title = str(instance.title), filename = filename
    )
    return file_path

class BlogPost(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False) 
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dislikes')

    def __str__(self):
        return self.title 
        #vraca naslov kad referenciramo objekt

class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null =True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.id:
            self.updated_at = datetime. datetime. now()
        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.author} - {self.post}"

#ako se izbrise blog post brise se i slika iz baze ili lokalne mreze/ servera
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
#radi slug prije nego je post commited u bazu
def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender = BlogPost) 
 