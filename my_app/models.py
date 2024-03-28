from django.db import models

class NewUser(models.Model):
    
    username = models.CharField(max_length=120,null=True,blank=True)
    first_name = models.CharField(max_length=120, blank=True,null=True)
    last_name = models.CharField(max_length=120, blank=True,null=True)
    email = models.EmailField(null=True,blank=True)
    Address = models.CharField(max_length=120,null=True,blank=True)
    password = models.CharField(max_length=20,blank=True,null=True)
    password_again = models.CharField(max_length=20,blank=True,null=True)


class TodoItems(models.Model):
    task_name = models.CharField(max_length=120,blank=True,null=True)
    due_date = models.DateTimeField(null=True,blank=True)
    task_type = models.CharField(max_length=120,null=True,blank=True)