from django.db import models
from django.forms import ModelForm
from django import forms

# Create your models here.	

class MyClass(models.Model):
	class_name = models.CharField(max_length=20)
	class_number = models.CharField(max_length=20)
	teacher = models.CharField(max_length=20)
	semester = models.CharField(max_length=20)
	#class_roster = models.ForeignKey(ClassRoster)
	
	authenticate = models.BooleanField(default=False)
	
	def __str__(self):
		return self.class_number

class user_info(models.Model):
	username = models.CharField(max_length=20)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	email = models.CharField(max_length=20)
	
	ADMIN = 'AD'
	TEACHER = 'TE'
	GRADER = 'GR'
	STUDENT = 'ST'

	USER_TYPE_CHOICES = (
		(ADMIN, 'Admin'),
		(TEACHER, 'Teacher'),
		(GRADER, "Grader"),
		(STUDENT, "Student"),
	)
	
	user_type = models.CharField (max_length=2, choices=USER_TYPE_CHOICES, default=STUDENT)
	password = models.CharField(max_length=20)
	authenticate = models.BooleanField(default=False)
	init_class_name = models.CharField(max_length=20)
	init_class_number = models.CharField(max_length=20)
	init_class_semester = models.CharField(max_length=20)

	class_list = models.ManyToManyField(MyClass)
	
	def __str__(self):
		return self.username
	
class ClassRoster(models.Model):
	student = models.ManyToManyField(user_info)
	in_class = models.OneToOneField(MyClass)
	class_name = models.CharField(max_length=20)
	class_number = models.CharField(max_length=20)	
	teacher = models.CharField(max_length=20)
	
	def __str__(self):
		return self.class_name + " : " + self.class_number
		
class AuthUser(models.Model):
	student_name = models.ForeignKey(user_info)
	class_name = models.ForeignKey(MyClass)
	authorized = models.BooleanField(default=False)

	def __str__(self):
		return self.student_name.username + " : " + self.class_name.class_name
	
class Assignment(models.Model):
	to_student = models.ForeignKey(user_info)
	to_class = models.ForeignKey(MyClass)
	is_owner = models.BooleanField(default=False)
	assignment_name = models.CharField(max_length=20)
	max_score = models.IntegerField(max_length=10)
	real_score = models.IntegerField(max_length=10)
	retry_limit = models.IntegerField(max_length=10, default=0)
	already_uploaded = models.BooleanField(default=False)
	already_graded = models.BooleanField(default=False)
	assign_date = models.DateField()
	due_date = models.DateField()

	def __str__(self):
		return self.to_class.class_number + " : " + self.to_student.username + " : " + self.assignment_name

class AssignmentFile(models.Model):
	to_assignment = models.ForeignKey(Assignment)
	my_file = models.FileField(upload_to='%Y/%m/%d')
	file_comment = models.CharField(max_length=200, blank=True)
	upload_number = models.IntegerField(max_length=10)
	date_uploaded = models.DateField()
		
class MyInbox(models.Model):
	sent_by = models.CharField(max_length=20)
	received_by = models.ForeignKey(user_info)
	date = models.DateField()
	title = models.CharField(max_length=40)
	message = models.CharField(max_length=350)
		
	def __str__(self):
		return self.title + " " + self.sent_by + " :: " + self.received_by.username
		
class MyOutbox(models.Model):
	sent_by = models.ForeignKey(user_info)
	received_by = models.CharField(max_length=20)
	date = models.DateField()
	title = models.CharField(max_length=40)
	message = models.CharField(max_length=350)
		
	def __str__(self):
		return "MESSAGE"

		
class UserForm(ModelForm):
    class Meta:
        model = user_info	
		
class class_roster(models.Model):
	user_id = models.ForeignKey(user_info)
	
class assignment_score(models.Model):
	user_id = models.ForeignKey(user_info)
	class_id = models.ForeignKey(class_roster)