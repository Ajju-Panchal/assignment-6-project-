from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('get_task_list/', views.get_task_list, name='get_task_list'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),

    # path('get_task/<int:task_id>/', views.get_task, name='get_task'),
    path('get_or_edit_task/<int:task_id>/', views.get_or_edit_task, name='get_or_edit_task'),
    path('logout/', views.logout_view, name='logout'),


]