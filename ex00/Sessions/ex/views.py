# ex/views.py
from django.shortcuts import render

def homepage(request):
    user_name = request.session.get('name', 'Guest')
    return render(request, 'ex/base.html', {'user_name': user_name})
