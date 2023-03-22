from django.urls import path

from like import views


urlpatterns = [
    path('', views.likeCreateView.as_view()),
    path('<int:pk>/', views.likeDeleteView.as_view()),
]