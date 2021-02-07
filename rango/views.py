from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category

from rango.models import Page


from rango.models import Question
from django.template import loader
from django.shortcuts import get_object_or_404

def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by the number of likes in descending order.
	# Retrieve the top 5 only -- or all if less than 5.
	# Place the list in our context_dict dictionary (with our boldmessage!)
	# that will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:6]
	
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage matches to {{ boldmessage }} in the template!
	context_dict={}
	context_dict ['boldmessage']= 'Crunchy, creamy, cookie, candy, cupcake!'
	context_dict['categories']=category_list
	context_dict['pages']=Page.objects.order_by('-views')[:5]
	
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render(request, 'rango/index.html', context=context_dict)

def about(request):
	return render(request, 'rango/about.html')
	
def show_category(request, category_name_slug):
	# Create a context dictionary which we can pass
	# to the template rendering engine.
	context_dict = {}
	
	try:
		# Can we find a category name slug with the given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# The .get() method returns one model instance or raises an exception.
		category= Category.objects.get(slug=category_name_slug)
		
		#Retrieve all of associated pages
		#the filter() will return a list of page objects or an empty list
		pages=Page.objects.filter(category=category)
		
		#Adds our results list to the template context under name pages
		context_dict['pages']=pages
		#also add the category object from the db to the context dictionary to verify
		#that the category exists
		context_dict['category']=category
	except Category.DoesNotExist:
		#if we didn't find the specified category don't do anything
		#the template will display the 'no category' message
		context_dict['category']=None
		context_dict['pages']=None
		
	#Go render the response and return it to client
	return render(request, 'rango/category.html', context=context_dict)
	
def detail(request , question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'rango/detail.html', {'question': question})

def results(request, question_id):
	response="You're looking at the results of question %s."
	return HttpResponse(response % question_id)
	
def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)

def index2(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'rango/index2.html', context)


	
	
	
	
	
