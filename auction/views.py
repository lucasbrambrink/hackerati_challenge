from django.shortcuts import render
from django.views.generic import TemplateView
from .models import InventoryItem

# Create your views here.

class AuctionView(TemplateView):
    template_name = 'auction/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'items': InventoryItem.objects.all()})



