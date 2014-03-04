##############################
# Imported Items #############
##############################
from __future__ import print_function
from time import strptime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core.context_processors import csrf
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.forms import EmailField
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from gradeapp.models import user_info, MyClass, UserForm, ClassRoster, AuthUser, Assignment, MyInbox, MyOutbox, AssignmentFile
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response
from gradeapp.forms import UploadFileForm
import sys
import datetime
import time

################################
# Begin Code ###################
################################
#Rule to Upload Files
def upload_file(request, number):
	#Check if user is authenticated
	if request.user.is_authenticated():
		try:
				myassignment = Assignment.objects.get(id=number)
		except:
				return HttpResponse("This page does not exist. e1")
	else:
		return redirect('register')
	#Check request method
	if request.method == 'POST':	
		retry = AssignmentFile.objects.filter(to_assignment=myassignment).count()
		if retry > myassignment.retry_limit:
			return HttpResponse("You already uploaded a file for this assignment and have exceeded the retry limit")
		else:
			MyFile = AssignmentFile(upload_number = retry+1, to_assignment = myassignment, my_file = request.FILES['datafile'], date_uploaded =  datetime.date.today())
			MyFile.save()
			myassignment.already_uploaded=True
			myassignment.save()
			return HttpResponseRedirect("/gradeapp/classes/"+myassignment.to_class.class_number+"/"+number+"/")
	else:
		return redirect('index')

#Return to the Index page
def index_page(request):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		return redirect('register')


#Create Assignment 
def create_assignment(request):
	#Checks user rights
	if not request.user.groups.filter(name='Admin') and not request.user.groups.filter(name = 'Teacher'):
		return HttpResponse("You do not have permission to access this page.")
	#Checks authentication
	elif request.user.is_authenticated():
		if request.method == 'POST':
			myclass_teacher = request.user.username
			myclass = MyClass.objects.get(id=request.POST['pass_class'])
			max_score = request.POST['max_score']
			real_score = 0
		
			try:
				due_date = datetime.datetime.strptime(request.POST['due_date'], "%B %d, %Y")			
			except:
				try:
					due_date = datetime.datetime.strptime(request.POST['due_date'], "%m-%d-%Y")			
				except:
					try: 
						due_date = datetime.datetime.strptime(request.POST['due_date'], "%m/%d/%Y")			
					except:
						return HttpResponse("Please enter the date in MM-DD-YYYY format.")

			create_date = datetime.date.today()
			
			#Checks if Assignment already exists
			if Assignment.objects.filter(assignment_name = request.POST['asg_name']).filter(to_class = myclass):
				return HttpResponse("Already exists.")
				
			#Tries to create assignment
			try:
				newAssignment = Assignment(is_owner = True, due_date = due_date, assign_date = create_date, assignment_name = request.POST['asg_name'], to_student = user_info.objects.get(username=request.user.username), to_class = myclass, max_score = max_score, real_score = real_score)
				newAssignment.save()
			except:
				message = "Error creating assignment!" 
				return render (request, "create_assignment.html", {"info": user_info.objects.all(), "roster": ClassRoster.objects.all(), "message": message})
				
			#Adds assignment for each member of the class roster
			for each_roster in ClassRoster.objects.all():
				if each_roster.in_class == myclass:
					for each_student in each_roster.student.all():
						if not each_student.username == request.user.username:
							newAssignment = Assignment(due_date = due_date, assign_date = create_date,assignment_name = request.POST['asg_name'], to_student = each_student, to_class = myclass, max_score = max_score, real_score = real_score)
							newAssignment.save()
			message = "Assignment added!" 
			return render (request, "create_assignment.html", {"info": user_info.objects.all(), "roster": ClassRoster.objects.all(), "message": message})
		else:
			return render (request, "create_assignment.html", {"info": user_info.objects.all(), "roster": ClassRoster.objects.all()})
	else:
		return redirect('register')
		
#Creates a new class
def create_a_class(request):
	#Checks user group rights
	if not request.user.groups.filter(name='Admin') and not request.user.groups.filter(name = 'Teacher'):
		return HttpResponse("You do not have permission to access this page.")
	#Checks authentication
	elif request.user.is_authenticated():
		#If authenticated, checks method type
		if request.method == 'POST':
			myclass_name = request.POST['class_name']
			myclass_number = request.POST['class_number']
			myclass_semester = request.POST['class_semester']
			creating_teacher = request.user.username
			new_class = MyClass(class_name = myclass_name, class_number = myclass_number, semester = myclass_semester, teacher = creating_teacher)
			new_class.save()				

			#Tries to create new roster
			try:
				newroster = ClassRoster(in_class = new_class, class_name = new_class.class_name, class_number = new_class.class_number, teacher=request.user.username) 
				newroster.save()
			except:
				return HttpResponse("...")

			#Updates teacher profile to add new class
			teacher_update = user_info.objects.get(username=request.user.username)
			teacher_update.class_list.add(new_class)
			teacher_update.save()

			return render (request, "create_a_class.html", {"info": user_info.objects.all()})			
		else:
			return render (request, "create_a_class.html", {"info": user_info.objects.all()})
	else:
		return redirect('register')

#Function to view classes
def classes(request):
	#Checks authentication
	if request.user.is_authenticated():
		myuser =  user_info.objects.get(username=request.user.username)
		return render (request, "class_list.html", {"myuser" : myuser, "classes": myuser.class_list.all()})
	else:
		return redirect('register')
		
#Function to view assignments
def view_assignment(request, string, number):
	#Checks authentication
	if request.user.is_authenticated():
		try:
				myclass = MyClass.objects.get(class_number=string)
				myuser =  user_info.objects.get(username=request.user.username)
				myassignment = Assignment.objects.get(id=number)
		except:
				return HttpResponse("This page does not exist. e1")
	else:
		return redirect('register')
	#Checks method 
	if request.method=='POST':
		#Checks post method for asg_max_score. Absence indicate update of information (not save) only
		if not 'asg_max_score' in request.POST:
			try: 
				newuser = user_info.objects.get(username=request.POST['pass_class'])
			except:
				return HttpResponse("This page does not exist. e42")
			asg_display= Assignment.objects.get(assignment_name = myassignment.assignment_name, to_student = newuser, to_class = myclass)			
			return render (request, "assignment_view.html", {"files": AssignmentFile.objects.all(), "myuser" : newuser, "myassignment" : asg_display, "all_assignments": Assignment.objects.filter(to_class=myclass).filter(assignment_name=myassignment.assignment_name), "myclass": myclass, "owner": myassignment.is_owner})	
		else:
			#Updates for all students
			if request.POST['update_user'] == request.user.username:
				update_query = Assignment.objects.filter(to_class = myclass).filter(assignment_name = myassignment.assignment_name)
				for each_assignment in update_query.all():
					each_assignment.max_score = request.POST['asg_max_score']
					each_assignment.assignment_name = request.POST['asg_name']
					each_assignment.due_date = datetime.datetime.strptime(request.POST['due_date'], "%B %d, %Y")
					each_assignment.retry_limit = request.POST['retry_limit']
					each_assignment.save()
					update_message = "The assignments have been updated for all stud."
				return redirect ('view_assignment', string, number)
			#Updates for a single student only
			else:
				update_user = user_info.objects.get(username = request.POST['update_user'])
				update_assignment = Assignment.objects.get(to_class = myclass, assignment_name = myassignment.assignment_name, to_student = update_user)
				update_assignment.max_score = request.POST['asg_max_score']
				update_assignment.real_score = request.POST['asg_score']
				update_assignment.due_date = datetime.datetime.strptime(request.POST['due_date'], "%B %d, %Y")
				update_assignment.retry_limit = request.POST['retry_limit']
				update_assignment.save()
				update_message = "The assignments have been updated for " + update_user.first_name + " " + update_user.last_name + "."
				return redirect ('view_assignment', string, number)
	#If method was not post, generates assignment view 
	else:
		if Assignment.objects.filter(id=number):
			if myassignment.to_class == myclass and myassignment.to_student.username == myuser.username and myclass.teacher == myuser.username:	
				return render (request, "assignment_view.html", {"files": AssignmentFile.objects.all(), "myuser" : myuser, "myassignment" : myassignment, "all_assignments": Assignment.objects.filter(to_class=myclass).filter(assignment_name=myassignment.assignment_name), "myclass": myclass})
			elif myassignment.to_class == myclass and myassignment.to_student.username == myuser.username:
				return render (request, "assignment_view.html", {"files": AssignmentFile.objects.all(), "myuser" : myuser, "myassignment" : myassignment})
			else:
				return HttpResponse("You do not have permission to access this page.")
		else: 
			return HttpResponse("This page does not exist. e2")

#Function to edit assignment
def edit_assignment(request, string, number):
	#Checks authentication
	if request.user.is_authenticated():
		#Finds assignment with given id to display
		if Assignment.objects.filter(id=number):
			try:
				myclass = MyClass.objects.get(class_number=string)
				myuser =  user_info.objects.get(username=request.user.username)
				myassignment = Assignment.objects.get(id=number)
			except:
				return HttpResponse("This page does not exist. e1")
			if myassignment.to_class == myclass and myassignment.is_owner:
				return render (request, "assignment_edit.html", {"myuser" : request, "myassignment" : myassignment})
			else:
				return HttpResponse("You do not have permission to access this page.")
		else: 
			return HttpResponse("This page does not exist. e2")
	else:
		return redirect('register')

#Function to generate assignment list		
def class_assignment(request, string):
	#Check to see is class exists
	try:
		myclass = MyClass.objects.get(class_number = string)
	except:
		return HttpResponse("Error loading class assignments. Please try again.")
	#If class exists, check authentication then show it
	if request.user.is_authenticated():
		myuser =  user_info.objects.get(username=request.user.username)
		return render (request, "assignment_list.html", {"myuser" : myuser, "myclass": myclass, "assignments": Assignment.objects.all()})
	else:
		return redirect('register')

#Function view for profile		
def view_profile_self(request):
	if request.user.is_authenticated():
		try:
			return redirect ('view_profile', request.user.username)
		except:
			return HttpResponse("Error: User doesn't exist.")
	else:
		return redirect('register')	

#Function view for inbox
def inbox(request):
	if request.user.is_authenticated():
		try:
			myuser =  user_info.objects.get(username=request.user.username)
			inbox = MyInbox.objects.filter(received_by=myuser)
			outbox = MyOutbox.objects.filter(sent_by=myuser)
			return render (request, 'inbox.html', {"myuser": myuser, "inbox": inbox.all(), "outbox": outbox.all()})
		except:
			return HttpResponse(request.user.username)
	else:
		return redirect('register')	

#Function view for message from inbox
def view_message(request, number):
	if request.user.is_authenticated():
		try:
			myuser =  user_info.objects.get(username=request.user.username)
			message = MyInbox.objects.get(id=number)
			return render (request, 'view_message.html', {"myuser": myuser, "mymessage": message})
		except:
			return HttpResponse(request.user.username)
	else:
		return redirect('register')	

#Function view for sending a message		
def send_message(request):
	if request.user.is_authenticated():
		try:
			myuser =  user_info.objects.get(username=request.user.username)
		except:
			return HttpResponse(request.user.username)
	else:
		return redirect('register')	
	if request.method == 'POST':
		send_to = user_info.objects.get(username=request.POST['send_to'])
		title = request.POST['title']
		message = request.POST['message']
		date =  datetime.date.today()
		
		new_inbox = MyInbox(sent_by = myuser.username, received_by = send_to, date = date, title = title, message = message)
		new_inbox.save()
		
		new_outbox = MyOutbox(sent_by = myuser, received_by = send_to.username, date = date, title = title, message = message)
		new_outbox.save()
		return render (request, 'send_message.html', {"myuser": myuser, "send_message": "Your message has been sent."})
		#except:
		#	return HttpResponse("1")
	else:
		return render (request, 'send_message.html', {"myuser": myuser})

#View for sending a message with given data.
#Probably superfluous, fix later
def send_message_id(request, number):
	if request.user.is_authenticated():
		try:
			myuser =  user_info.objects.get(username=request.user.username)
			message = MyInbox.objects.get(id=number)
		except:
			return HttpResponse(request.user.username)
	else:
		return redirect('register')	
	if request.method == 'POST':
		send_to = user_info.objects.get(username=request.POST['send_to'])
		title = request.POST['title']
		message = request.POST.get("message")
		date =  datetime.date.today()
		
		new_inbox = MyInbox(sent_by = myuser.username, received_by = send_to, date = date, title = title, message = message)
		new_inbox.save()
	
		new_outbox = MyOutbox(sent_by = myuser, received_by = send_to.username, date = date, title = title, message = message)
		new_outbox.save()
		return render (request, 'send_message.html', {"myuser": myuser, "send_message": "Your message has been sent."})
	else:
		return render (request, 'send_message.html', {"myuser": myuser, "message": message})
			
#Function to view profile of a given user of string
def view_profile(request, string):
	if request.user.is_authenticated():
		try:
			myuser =  user_info.objects.get(username=string)
		except:
			return HttpResponse("Error: User doesn't exist.")
	else:
		return redirect('register')	
	if request.user.username == string:
		#Updates information if done through post
		if request.method == 'POST':
			f_name = request.POST['first_name']
			l_name = request.POST['last_name']
			email = request.POST['email']
			update_user = request.POST['update_user']
			update_info = user_info.objects.get(username=update_user)
			update_user = User.objects.get(username=update_user)
			update_info.first_name = f_name
			update_info.last_name = l_name
			update_info.email = email
			update_info.save()
			update_user.first_name = f_name
			update_user.last_name = l_name
			update_user.email_address = email
			update_user.save()
			return redirect ('view_profile', myuser.username)
		else:
			return render (request, "edit_profile.html", {"myuser": myuser, "classes": myuser.class_list.all()})
	else:
		return render(request, "view_profile.html", {"myuser": myuser, "classes": myuser.class_list.all()})

#Function to add a class for a student		
def add_a_class(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			myclass_name = request.POST['class_name']
			myclass_number = request.POST['class_number']
			myclass_semester = request.POST['class_semester']			
			#updates class info for original user
			try: 
				new_class = MyClass.objects.get(class_name = myclass_name, class_number = myclass_number, semester = myclass_semester)
			except:
				error_message = "Please check your data and try adding the class again."
				return render (request, "add_a_class.html", {"info": user_info.objects.all(), "message": error_message})			
			
			new_student = user_info.objects.get(username=request.user.username)
			
			#checks if you already tried to add the class
			if AuthUser.objects.filter(class_name = new_class).filter(student_name = new_student):
				error_message = "You have already tried to add this class. Please wait for a teacher response."
				return render (request, "add_a_class.html", {"info": user_info.objects.all(), "message": error_message})			
			
			new_auth_ticket = AuthUser(class_name = new_class, student_name = new_student)
			new_auth_ticket.save()
					
			#updates class roster
			try:
				newroster = ClassRoster.objects.get(in_class = new_class, class_name = myclass_name, class_number = myclass_number, teacher = new_class.teacher) 
				newroster.student.add(user_info.objects.get(username=request.user.username))
				newroster.save()
			except:
				error_message = "There was an error adding your to the class. Please try again."
				return render (request, "add_a_class.html", {"info": user_info.objects.all(), "message": error_message})			

			#adds class to user data
			try:
				myuser = user_info.objects.get(username=request.user.username)
				myuser.class_list.add(new_class)
				myuser.save()
			except:
				error_message = "There was an error adding your to the class. Please try again."
				return render (request, "add_a_class.html", {"info": user_info.objects.all(), "message": error_message})			
			
			create_added_student_message(new_class, myuser)
			
			return render (request, "add_a_class.html", {"info": user_info.objects.all(), "message": "You have added " + myclass_number + ". Please wait for teacher approval before further action."})			
		else:
			return render (request, "add_a_class.html", {"info": user_info.objects.all()})
	else:
		return redirect('register')

#Simple log out function
def log_out(request):
	logout(request)
	return HttpResponse("You have been logged out.")

#Base index view	
def index(request):
	if request.user.is_authenticated():
		return render (request, "index.html", {"info": user_info.objects.all()})
	else:
		return redirect('register')

#Admin function to authorize teacher
def auth_myuser(request):
	if not request.user.groups.filter(name='Admin'):	
		return HttpResponse("You do not have permission to access this page.")
	elif request.user.is_authenticated():
		if request.method == 'POST':
			myaction = request.POST['action']
			myname = request.POST['user']
			edit_user = User.objects.get(username=myname)
			moreinfo = user_info.objects.get(username=myname)
			if myaction == 'remove_teacher':
				mygroup = Group.objects.get(name='Teacher')
				edit_user.groups.remove(mygroup)	
				edit_user.save()
				moreinfo.authenticate = False
				moreinfo.save()
				return render (request, "authenticate.html", {"info": user_info.objects.all()})
			elif myaction == 'add_teacher':
				mygroup = Group.objects.get(name='Teacher')
				edit_user.groups.add(mygroup)	
				edit_user.save()
				moreinfo.authenticate = True
				newclass = MyClass(class_name = moreinfo.init_class_name, class_number = moreinfo.init_class_number, semester = moreinfo.init_class_semester, teacher = moreinfo.username, authenticate = True)
				newclass.save()
				newroster = ClassRoster(in_class = newclass, class_name = newclass.class_name, class_number = newclass.class_number, teacher=moreinfo.username) 
				newroster.save()
				newroster.student.add(moreinfo)
				moreinfo.save()
				
				date = datetime.date.today()
				title = "Account Approved."
				message = "Your account has been approved and is now operable."
				new_inbox = MyInbox(sent_by = "ADMIN", received_by = moreinfo, date = date, title = title, message = message)
				new_inbox.save()

				moreinfo.class_list.add(newclass)

				return render (request, "authenticate.html", {"info": user_info.objects.all()})
			else:
				return HttpResponse("Hi")
		else:
			return render (request, "authenticate.html", {"info": user_info.objects.all()})
	else:
		return redirect('register')

#Teacher function to approve student for class
def approve_student_for_class(request, string):
	if request.user.is_authenticated():
		class_num = string
		try:
			myclass = MyClass.objects.get(class_number = class_num, teacher = request.user.username) 
		except:
			return HttpResponse("This page does not exist or you do not have access to this page. Please check your url and try again.")
		if request.method == 'POST':
			myaction = request.POST['action']
			myname = request.POST['user']
			edit_user = User.objects.get(username=myname)
			moreinfo = user_info.objects.get(username=myname)
			auth_user = AuthUser.objects.get(student_name = moreinfo, class_name = myclass)
			if myaction == 'remove_student':
				auth_user.authorized = False
				auth_user.delete()
				
				moreinfo.class_list.remove(myclass)
				moreinfo.save()
				
				roster = ClassRoster.objects.get(in_class = myclass)
				roster.student.remove(moreinfo)
				roster.save()
				
				#deletes assignments when student is removed
				for each_assignment in Assignment.objects.all():
					if each_assignment.to_student.username == edit_user.username and each_assignment.to_class == myclass:
						each_assignment.delete()

				date = datetime.date.today()
				title = "Removed from Class " + myclass.class_number
				message = "Your have been removed from " + myclass.class_number + " by the instructor."
				new_inbox = MyInbox(sent_by = "ADMIN", received_by = moreinfo, date = date, title = title, message = message)
				new_inbox.save()

				return render (request, "approve_student_for_class.html", {"info": user_info.objects.all(), "auth": AuthUser.objects.all(), "instance_class": myclass})
			elif myaction == 'add_student':
				mygroup = Group.objects.get(name='Student')
				edit_user.groups.add(mygroup)	
				edit_user.save()
				moreinfo.authenticate = True
				auth_user.authorized = True
				moreinfo.save()
				auth_user.save()
				
				date = datetime.date.today()
				title = "Account Approved."
				message = "Your have been added to " + myclass.class_number + "."
				new_inbox = MyInbox(sent_by = "ADMIN", received_by = moreinfo, date = date, title = title, message = message)
				new_inbox.save()

				#adds assignments when student is added to class
				for each_assignment in Assignment.objects.all():
					if each_assignment.to_student.username == myclass.teacher and each_assignment.to_class == myclass:
						new_assignment_instance = Assignment(assign_date = each_assignment.assign_date, due_date = each_assignment.due_date, to_student = moreinfo, to_class = myclass, assignment_name = each_assignment.assignment_name, max_score = each_assignment.max_score, real_score = 0, retry_limit = each_assignment.retry_limit)
						new_assignment_instance.save()		
				return render (request, "approve_student_for_class.html", {"info": user_info.objects.all(), "auth": AuthUser.objects.all(), "instance_class": myclass})
			else:
				return HttpResponse("Hi")
		else:
				return render (request, "approve_student_for_class.html", {"info": user_info.objects.all(), "auth": AuthUser.objects.all(), "instance_class": myclass})
	else:
		return redirect('register')	
		
#Shows class list for instructor for classes he or she may have.
#Class list is to manage students from each of those classes.
def approve_student(request):
	if request.user.is_authenticated():
		myuser =  user_info.objects.get(username=request.user.username)
		return render (request, "class_list.html", {"myuser" : myuser, "classes": myuser.class_list.all()})
	else:
		return redirect('register')	

#Function to approve grader
def approve_grader(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			myaction = request.POST['action']
			myname = request.POST['user']
			edit_user = User.objects.get(username=myname)
			moreinfo = user_info.objects.get(username=myname)
			if myaction == 'remove_grader':
				mygroup = Group.objects.get(name='Student')
				edit_user.groups.remove(mygroup)	
				edit_user.save()
				moreinfo.authenticate = False
				moreinfo.save()
				return render (request, "approve_graders.html", {"info": user_info.objects.all()})
				#mygroup.user_set.add(myname)
			elif myaction == 'add_grader':
				mygroup = Group.objects.get(name='Student')
				edit_user.groups.add(mygroup)	
				edit_user.save()
				moreinfo.authenticate = True
				moreinfo.save()
				return render (request, "approve_graders.html", {"info": user_info.objects.all()})
			else:
				return HttpResponse("Hi")
		else:
			return render (request, "approve_graders.html", {"info": user_info.objects.all()})
	else:
		return redirect('register')		
			
#Login user
#Rename and change other names later for consistency/ease of understanding
def log(request):
	if request.method == 'POST':
		username = request.POST['userlog']
		userpass = request.POST['passlog']
		if login_user(request, username, userpass):
			return redirect('index')
		else:
			return HttpResponse("Your information could not be authenticated. Please try again.")
	else:
		return HttpResponse("Your information could not be authenticated. Please try again.")
		
#Register function to register all new users		
def register(request):
	if request.user.is_authenticated():
		return redirect('index')
	elif request.method == 'POST':
		stuff = request.POST
		username = stuff['userreg']
		password = stuff['passreg']
		first_name = stuff['namereg']
		email = stuff['email']
		user_type = stuff['type']
		lname = stuff["lastname"]
		init_class = stuff['class_name']
		init_num = stuff['class_number']
		init_sem = stuff['class_semester']
		user = user_info.objects.filter(username=username)
		
		#Checks if Email Address if valid
		if not isEmailAddressValid(email):	
			error_message = "ERROR: Your email " + email + " was not valid. Please enter a valid email and try again."
			return render(request, 'register.html', {"error":error_message})
		#Check if fields are left blank
		if username == "" or first_name=="" or lname =="" or email =="" or password == "":
			error_message = "ERROR: One or more fields were left empty. Please fill out each field and try again."
			return render(request, 'register.html', {"error":error_message})
		#Check if user already exists
		elif user.exists():
			error_message = "ERROR: A user already exists with the given username. Enter a new username and try again."
			return render(request, 'register.html', {"error":error_message})
		#Creates our user 
		else:

			#Creates user for user_info table
			cost_obj = user_info(init_class_name = init_class, init_class_number= init_num, init_class_semester = init_sem, username=username, password=password, first_name=first_name, last_name=lname, email=email, user_type=user_type)
			cost_obj.save()

			#Creates user for Auth table
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = lname
			user.save()

			#Adds student or grader to the class as unauthorized student(teacher needs to be approved before class creation)
			if user_type != "TE":
				find_class = MyClass.objects.get(class_name = init_class, class_number = init_num, semester= init_sem)
				authorize_user = AuthUser(student_name = cost_obj, class_name = find_class)
				authorize_user.save()
				cost_obj.class_list.add(find_class)
				create_added_student_message(find_class, cost_obj)

			create_welcome_message(cost_obj)
			if login_user(request, username, password):
				return redirect('index')
			else:
				return redirect('register')
	else:
		return TemplateResponse (request, "register.html")

####################
#General Functions #
####################
#Creates an "Student Added Class" message to send to instructor
def create_added_student_message(added_class, student):
	date = datetime.date.today()
	title = "New Student for " + added_class.class_number
	teacher = user_info.objects.get(username=added_class.teacher)
	message = student.first_name + " " + student.last_name + " has added you to " + added_class.class_number + "."
	generate_inbox_message("ADMIN", teacher, date, title, message)

#Creates a welcome message for all new users.	
def create_welcome_message(new_user):
	date = datetime.date.today()
	title = "Welcome to The Grading System!"
	message = "Welcome to the grading system. Before you can use our website in full, you will need to be approved. Until then, you will not have access to your classes or assignments."
	generate_inbox_message("ADMIN", new_user, date, title, message)

#Generates an inbox message when given necessary data
def generate_inbox_message(sent_by, received_by, date, title, message):
	new_inbox = MyInbox(sent_by = sent_by, received_by = received_by, date = date, title = title, message = message)
	new_inbox.save()

#Checks to see if e-mail address if valid
def isEmailAddressValid( email ):
	try:
		EmailField().clean(email)
		return True
	except ValidationError:
		return False

#Function that sees if user can be authenticated and then logs in user. 		
def login_user(request, username, password):
	try:
		myuser = authenticate(username = username, password = password)
		if myuser is not None:
			if myuser.is_active:
				login(request, myuser)
				return True
			else:
				return False
		else:
			return False
	except:
		return False
		

##############################
# Deleted/Outdated Functions #
################################################################################
#Old Approve Student function for all student for all classes on one page      #
#No longer used/needed. Commented in case error/need	                       #
################################################################################
#def approve_studentxy(request):
#	if request.user.is_authenticated():
#		if request.method == 'POST':
#			myaction = request.POST['action']
#			myname = request.POST['user']
#			class_num = request.POST['my_class']
#			edit_user = User.objects.get(username=myname)
#			moreinfo = user_info.objects.get(username=myname)
#			myclass = MyClass.objects.get(class_number = class_num, teacher = request.user.username) 
#			auth_user = AuthUser.objects.get(student_name = moreinfo, class_name = myclass)
#			if myaction == 'remove_student':
#				#mygroup = Group.objects.get(name='Student')
#				#edit_user.groups.remove(mygroup)	
#				#edit_user.save()
#				auth_user.authorized = False
#				auth_user.delete()
#				
#				moreinfo.class_list.remove(myclass)
#				moreinfo.save()
#				
#				roster = ClassRoster.objects.get(in_class = myclass)
#				roster.student.remove(moreinfo)
#				roster.save()
#				
#				#deletes assignments when student is removed
#				for each_assignment in Assignment.objects.all():
#					if each_assignment.to_student.username == edit_user.username and each_assignment.to_class == myclass:
#						each_assignment.delete()
#				return render (request, "approve_students.html", {"info": user_info.objects.all(), "auth": AuthUser.objects.all(), "classes": MyClass.objects.all()})
#				#mygroup.user_set.add(myname)
#			elif myaction == 'add_student':
#				mygroup = Group.objects.get(name='Student')
#				edit_user.groups.add(mygroup)	
#				edit_user.save()
#				moreinfo.authenticate = True
#				auth_user.authorized = True
#				moreinfo.save()
#				auth_user.save()
#				
#				date = datetime.date.today()
#				title = "Account Approved."
#				message = "Your have been added to " + myclass.class_number + "."
#				new_inbox = MyInbox(sent_by = "ADMIN", received_by = moreinfo, date = date, title = title, message = message)
#				new_inbox.save()
#
#				#adds assignments when student is added to class
#				for each_assignment in Assignment.objects.all():
#					if each_assignment.to_student.username == myclass.teacher and each_assignment.to_class == myclass:
#						new_assignment_instance = Assignment(assign_date = each_assignment.assign_date, due_date = each_assignment.due_date, to_student = moreinfo, to_class = myclass, assignment_name = each_assignment.assignment_name, max_score = each_assignment.max_score, real_score = 0, retry_limit = each_assignment.retry_limit)
#						new_assignment_instance.save()		
#				return render (request, "approve_student_for_class.html", {"info": user_info.objects.all(), "auth": AuthUser.objects.all(), "instance_class": myclass})
#			else:
#				return HttpResponse("Hi")
#		else:
#			return render (request, "approve_students.html", {"info": user_info.objects.all(), "auth" : AuthUser.objects.all(), "classes": MyClass.objects.all()})
#	else:
#		return redirect('register')