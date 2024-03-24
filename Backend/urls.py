from django.urls import path
from .views import process_user_input_data

urlpatterns = [
    path('process_user_input_data/', process_user_input_data, name='process_user_input_data'),
]