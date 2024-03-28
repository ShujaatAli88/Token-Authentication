from django.urls import path
from my_app import views


urlpatterns = [
    path('new_user/',views.SignUp.as_view(),name='signup'),
    path('login/',views.Login.as_view(),name='login'),
    path('user/',views.GetUser.as_view(),name='get-user'),
    path('logout/',views.LogoutUser.as_view(),name='logout'),
    path('email/',views.GetEmail.as_view(),name='email'),
    path('password_update/',views.UpdatePassword.as_view(),name='pass-update'),
    path('add_todo_tasks/',views.AddTask.as_view(),name='add-todo'),
    path('get_todo/',views.GetTodoItems.as_view(),name='get-tasks'),
]
