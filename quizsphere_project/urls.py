from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "QuizSphere Administration"
admin.site.site_title = "QuizSphere Admin Portal"
admin.site.index_title = "QuizSphere Management & Evaluation System"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
]
