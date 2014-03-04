from django.contrib import admin
from gradeapp.models import user_info, MyClass, UserForm, ClassRoster, AuthUser, Assignment, MyInbox, MyOutbox, AssignmentFile

# Register your models here.
admin.site.register(user_info)
admin.site.register(MyClass)
admin.site.register(ClassRoster)
admin.site.register(AuthUser)
admin.site.register(MyInbox)
admin.site.register(MyOutbox)
admin.site.register(AssignmentFile)
admin.site.register(Assignment)