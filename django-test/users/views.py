from django.contrib import auth
from django.views import generic
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import forms as auth_forms
from django.contrib import messages

_error_message = "%s : %s"


# class ContextUserMixinView(generic.TemplateView):
#     def get_context_data(self, *args, **kwargs):
#         """
#         Insert the User object into the context dict.
#         """
#         context = {}
#         if 'user' not in kwargs:
#             pass
#             # context['user'] = getattr(self, request).user
#         context.update(kwargs)
#         return super(ContextUserMixinView, self).get_context_data(**context)


# class TemplateContextUserMixinView(generic.TemplateView):
#     def get_context_data(self, **kwargs):
#         context = super(TemplateContextUserMixinView, self).get_context_data(**kwargs)
#         if 'user' not in context:
#             context['user'] = self.request.user
#         return context


class NewLogInView(generic.TemplateView):
    pass


class LogInView(generic.TemplateView):
    template_name = 'users/login.html'

    # def get_context_data(self, **kwargs):
    #     context = super(LogInView, self).get_context_data(**kwargs)
    #     if 'user' not in context:
    #         context['user'] = self.request.user
    #     return context

    def get(self, request, *args, **kwargs):
        next = request.GET.get('next',request.session.get('next','/'))
        request.session['next'] = next
        if request.user.is_authenticated():
            return redirect(next)
        else:
            return super(LogInView, self).get(request, *args, **kwargs)

    def post(self, request, *arg, **kwargs):
        if not request.user.is_authenticated():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect(request.session.get('next','/'))
                else:
                    messages.error(request, "Account is not active!")
                    return redirect(reverse('users:login'))
            else:
                # Return an 'invalid login' error message.
                messages.error(request, "Invalid login!")
                return redirect(reverse('users:login'))
        else:
            return redirect('/')


class LogOutView(generic.View):
    def get(self, request, *arg, **kwargs):
        if request.user.is_authenticated():
            auth.logout(request)
            return redirect('users:login')
        return redirect('/')


# class UserMixinView(generic.base.ContextMixin, generic.View):
#
#     def get_context_data(self, **kwargs):
#         context = {}
#         if 'user' not in kwargs:
#             context['user'] = self.request.user
#         context.update(kwargs)
#         return super(UserMixinView, self).get_context_data(**context)


class DetailView(generic.TemplateView):
    template_name = "users/detail.html"


class SignInView(generic.TemplateView):
    template_name = "users/sign_in.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('users:profile')
        return super(SignInView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = auth_forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, _error_message % (field, error))
        return redirect('users:signin')
