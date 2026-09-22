from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('quiz/<slug:slug>/', views.quiz_detail, name='category_detail'),
    path('quiz/<slug:slug>/start/', views.quiz_take, name='quiz_take'),
    path('quiz/<slug:slug>/submit/', views.quiz_submit, name='quiz_submit'),
    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Presentation & Architecture Showcase (from PPTX)
    path('project-presentation/', views.presentation_showcase, name='presentation_showcase'),
]
