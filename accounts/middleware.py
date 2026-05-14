from django.contrib.auth import logout
from django.shortcuts import redirect
import time

SESSION_TIMEOUT = 600  # 10 minutes in seconds

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            current_time = time.time()

            if last_activity and (current_time - last_activity > SESSION_TIMEOUT):
                logout(request)
                return redirect('login')  # change to your login url name

            request.session['last_activity'] = current_time

        return self.get_response(request)