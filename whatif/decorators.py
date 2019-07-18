
def check_login(function):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user'):
            return redirect('login')
        else:
            return function(request, *args, **kwargs)
        # wrapper.__doc__ = function.__doc__
        # wrapper.__name__ = function.__name__
        return wrapper