from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import HackeratiUser
from django.http import JsonResponse
import json
from faker import Faker
from .utils import FormatHelper as fh

# Create your views here.

class OnBoardingView(TemplateView):
    template_name = 'base/on_boarding.html'
    faker = Faker()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {

        })

    def post(self, request, *args, **kwargs):
        print(request)
        # session_id = request.SESSION
        post = json.loads(request.POST['data'])
        print post

        if not len(post['name']):
            name = self.faker.name()

        if not len(post['username']):
            username = fh.name_to_username(name)

        if not len(post['password']):
            password = "".join(self.faker.words())

        user = HackeratiUser(
            name=name,
            username=username
        )
        user.set_password(raw_password=password)

        # user.save()
        return JsonResponse({
            'user_data': {'name': user.name, 'username': user.username},
        })
