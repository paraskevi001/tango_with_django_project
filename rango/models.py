from django.db import models
import datetime
from django.utils import timezone
from django.template.defaultfilters import slugify

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		self.slug=slugify(self.name)
		super(Category,self).save(*args,**kwargs)
	
	class Meta:
		verbose_name_plural = 'categories'
	
	def __str__(self):
		return self.name
	
class Page(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	
	def __str__(self):
		return self.title
		
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	
	def __str__(self):
		return self.question_text
		
	def was_published_recently(self):
		now=timezone.now()
		return now-datetime.timedelta(days=1)<=self.pub_date<=now
	was_published_recently.admin_order_field='pub_date'
	was_published_recently.boolean=True
	was_published_recently.short_description='Published recently?'


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	
	def __str__(self):
		return self.choice_text
