from django.urls import path
from . import views

app_name = 'voting_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('vote/', views.vote_list, name='vote_list'),
    path('vote/<int:candidate_id>/', views.vote_candidate, name='vote_candidate'),
    path('results/', views.results, name='results'),
    path('logout/', views.user_logout, name='logout'),
]
