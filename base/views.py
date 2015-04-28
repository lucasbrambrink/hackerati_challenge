from django.shortcuts import render, redirect
from django.views.generic import TemplateView

# Create your views here.

class OnBoardingTemplate(TemplateView):
    template_name = 'base/on_boarding.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {

        })

    def post(self, request, *args, **kwargs):
        post = request.POST
        return redirect('auction')
