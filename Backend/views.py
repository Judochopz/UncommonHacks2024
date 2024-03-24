# views.py

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserInputData

def process_user_input_data(request):
    if request.method == 'POST':
        form = UserInputData(request.POST)
        if form.is_valid():
            # Process the form data here
            # Access form data using form.cleaned_data dictionary
            genre_data = form.cleaned_data['genre_data']
            username_data = form.cleaned_data['username_data']
            # Redirect or render response as needed
            return HttpResponseRedirect('/success/')  # Change /success/ here to the success URL
    else:
        form = UserInputData()
    return render(request, 'my_template.html', {'form': form}) # not sure what to do here
