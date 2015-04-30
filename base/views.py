from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
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

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
        }, RequestContext(request))


class OnBoardingAPI(View):
    faker = Faker()

    def post(self, request, action, *args, **kwargs):
        post = json.loads(request.POST['data'])

        if action == 'new':
            username = post['username']

            user = HackeratiUser.objects.filter(username=username).first()
            if not user:
                name = post['name']
                if not len(name):
                    name = self.faker.name()

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

        elif action == 'info':
            username = post['username']
            password = post['password']
            if not password or not len(password):
                print(username, password)
                count = HackeratiUser.objects.filter(username__contains=username).count()
                credential = 'username'
                print(count)
                valid = count > 0
                print(valid)
            elif len(password):
                user = HackeratiUser.objects.get(username=username)
                valid = user.check_password(password)
                credential = 'password'

            return JsonResponse({
                'data': {'credential': credential, 'valid': valid},
            })






