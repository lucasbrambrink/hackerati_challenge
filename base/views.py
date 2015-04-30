from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.template import RequestContext
from .models import HackeratiUser
from django.http import JsonResponse
import json
from faker import Faker
from .utils import FormatHelper as fh
import datetime
# Create your views here.

class OnBoardingView(TemplateView):
    template_name = 'base/on_boarding.html'
    faker = Faker()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
        }, RequestContext(request))

    def post(self, request, *args, **kwargs):
        post = json.loads(request.POST['data'])

        name = post['name']
        if not len(name):
            name = self.faker.name()

        username = post['username']
        if not len(post['username']):
            username = fh.name_to_username(name)

        password = post['password']
        if not len(post['password']):
            password = "".join(self.faker.words())


        user = HackeratiUser(
            name=str(name),
            username=str(username)
        )
        user.set_password(raw_password=str(password))
        user.last_login = datetime.datetime.now()
        user.save()

        request.session['id'] = user.pk
        return JsonResponse({
            'user_data': {'name': user.name, 'username': user.username},
        })
