# ex/middleware.py
import random
from django.conf import settings
from datetime import datetime, timedelta

class RandomNameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session = request.session
        current_time = datetime.now()

        if 'name' not in session or 'expiry' not in session or datetime.strptime(session['expiry'], '%Y-%m-%d %H:%M:%S') < current_time:
            session['name'] = random.choice(settings.NAMES)
            session['expiry'] = (current_time + timedelta(seconds=42)).strftime('%Y-%m-%d %H:%M:%S')
            session.save()

        response = self.get_response(request)
        return response
