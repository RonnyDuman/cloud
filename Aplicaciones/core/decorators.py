from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_token'):
            return redirect('loginIn')  # o tu login general
        return view_func(request, *args, **kwargs)
    return wrapper
