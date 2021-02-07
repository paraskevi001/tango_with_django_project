from django.contrib import admin
from rango.models import Category, Page
from rango.models import Choice,Question
# Register your models here.



	
class PageAdmin(admin.ModelAdmin):
	fieldsets = [
        (None,{'fields': ['title']}),
        (None,{'fields':['url']}),
    	] 
	
	list_display=('title','category','url')
	
	
admin.site.register(Page,PageAdmin)

class ChoiceInline(admin.TabularInline):
	model=Choice
	extra=3
	
class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    	] 
	inlines = [ChoiceInline]
	list_display=('question_text','pub_date','was_published_recently')
	list_filter=['pub_date']
	search_fields=['question_text']
	
admin.site.register(Question,QuestionAdmin)

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields={'slug':('name',)}
	
admin.site.register(Category,CategoryAdmin)

