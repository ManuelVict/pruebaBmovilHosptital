from django.shortcuts import redirect
class SuperUSerMixin(object): 
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')

class IsLogin(object):
    def dispatch(self, request, *args, **kwargs):
        if not  request.user.is_authenticated:
            return super().dispatch(request,*args, **kwargs)
        return redirect('index')
    