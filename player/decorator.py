from django.shortcuts import redirect

def user_type_required(user_type):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = request.user

            if user.user_type in user_type:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('staff_dashboard')

        return wrapper

    return decorator