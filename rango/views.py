from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm,PageForm
from django.shortcuts import redirect
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from rango.models import Choice,Question
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from datetime import datetime

def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by the number of likes in descending order.
	# Retrieve the top 5 only -- or all if less than 5.
	# Place the list in our context_dict dictionary (with our boldmessage!)
	# that will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage matches to {{ boldmessage }} in the template!
	context_dict={}
	context_dict ['boldmessage']= 'Crunchy, creamy, cookie, candy, cupcake!'
	context_dict['categories']=category_list
	context_dict['pages'] = page_list
	
	visitor_cookie_handler(request)
	
	
	response = render(request, 'rango/index.html', context=context_dict)
	
	return response

def about(request):
	print(request.method)
	print(request.user)
	if request.session.test_cookie_worked():
		print("TEST COOKIE WORKED!")
		request.session.delete_test_cookie()
	visitor_cookie_handler(request)
	context_dict={}
	context_dict['visits'] = request.session['visits']
	
	return render(request, 'rango/about.html',context=context_dict)
	
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
	
@login_required	
def add_category(request):
	form=CategoryForm()
	
	#A HTTP POST
	if request.method=='POST':
		form=CategoryForm(request.POST)
		#Have we been provided with a valid form?
		if form.is_valid():
			#save the new category to the database
			form.save(commit=True)
			#now that the category is saved, we could confirm this
			#for now, redirect the user back to the index view
			return redirect('/rango/')
		else:
		#the supplied form contained errors-just print them to the terminal
			print(form.errors)
		#Will handle the bad form,new form or no form supplied cases
		#Render the form with error messages(if any)
	return render(request, 'rango/add_category.html', {'form': form})

@login_required		
def add_page(request, category_name_slug):
	try:
		category=Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category=None
	
	#You cannot add a page to a category that does not exist
	if category is None:
		return redirect('/rango/')
	
	form=PageForm()
	
	if request.method=='POST':
		form=PageForm(request.POST)
		
		if form.is_valid():
			if category:
				page=form.save(commit=False)
				page.category=category
				page.views=0
				page.save()
				return redirect(reverse('rango:show_category',
					kwargs={'category_name_slug':category_name_slug}))
		else:
			print(form.errors)
				
	context_dict={'form':form,'category':category}
	return render(request, 'rango/add_page.html', context=context_dict)
	
def register(request):
	registered=False
	if request.method=='POST':
		user_form=UserForm(request.POST)
		profile_form=UserProfileForm(request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()
			
			user.set_password(user.password)
			user.save()
			
			profile=profile_form.save(commit=False)
			profile.user=user
			
			if 'picture' in request.FILES:
				profile.picture=request.FILES['picture']
			
			profile.save()
			registered=True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form=UserForm()
		profile_form=UserProfileForm()
	
	return render(request, 'rango/register.html', 
			context={ 'user_form': user_form, 'profile_form': profile_form,
					'registered':registered})

def user_login(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		
		if user:
			if user.is_active:
				login(request,user)
				return redirect(reverse('rango:index'))
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:
			print(f"Invalid login details: {username},{password}")
			return HttpResponse("invalid login details supplied.")
	else:
		return render(request,'rango/login.html')

@login_required
def restricted(request):
		return render(request,'rango/restricted.html')
	
@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('rango:index'))

def get_server_side_cookie(request,cookie,default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

def visitor_cookie_handler(request):
	visits = int(get_server_side_cookie(request, 'visits', '1'))
	
	last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
	last_visit_time=datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
	
	if (datetime.now() - last_visit_time).days>0:
		visits=visits+1
		request.session['last_visit'] = str(datetime.now())
	else:
		request.session['last_visit'] = last_visit_cookie
	
	request.session['visits'] = visits


class Index2View(generic.ListView):
	template_name='rango/index2.html'
	context_object_name = 'latest_question_list'
	
	def get_queryset(self):
		"""Return the last five published questions."""
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model=Question
	template_name='rango/detail.html'
	
class ResultsView(generic.DetailView):
	model=Question
	template_name='rango/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		return render(request, 'rango/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
	else:
        	selected_choice.votes += 1
        	selected_choice.save()
        	return HttpResponseRedirect(reverse('rango:results', args=(question.id,)))	
	
	
