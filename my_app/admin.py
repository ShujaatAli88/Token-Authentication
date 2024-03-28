from django.contrib import admin
from my_app.models import NewUser ,TodoItems

class NewUserAdmin(admin.ModelAdmin):
    list_display = ["first_name","last_name","email","Address"]

class TodoAdmin(admin.ModelAdmin):
    list_display = ["task_name","task_type"]

admin.site.register(NewUser,NewUserAdmin)
admin.site.register(TodoItems, TodoAdmin)