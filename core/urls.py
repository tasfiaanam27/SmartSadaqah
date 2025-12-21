from django.urls import path
from . import views

urlpatterns = [
    path('', views.approved_case_list, name='home'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<int:project_id>/', views.case_detail, name='project_detail'),
    path('projects/<int:project_id>/donate/', views.donate_to_case, name='donate_to_project'),
    path('completed/', views.completed_projects, name='completed_projects'),
    path('completed/<int:project_id>/', views.completed_project_detail, name='completed_project_detail'),
    path('recipient/request/', views.recipient_request_view, name='recipient_request'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact, name='contact'),
]
