from django.urls import path
from . import views

app_name = 'surveys'
urlpatterns = [
    path('', views.SurveyListView.as_view(), name='list'),
    path('new/', views.SurveyCreateView.as_view(), name='create'),
    path('<int:pk>/respond/', views.SurveyRespondView.as_view(), name='respond'),
    path('<int:pk>/results/', views.SurveyResultsView.as_view(), name='results'),
    path('<int:pk>/results/<int:response_pk>/', views.SurveyResponseDetailView.as_view(), name='response_detail'),
]
