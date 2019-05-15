from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from search.forms import SearchForm


@method_decorator(csrf_exempt, name='dispatch')
class MainList(View):
    def get(self, request):
        print('####')
        form = SearchForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        print('post')
        print(request.POST['company_name'])
        print(request.POST['keywords'])
        return render(request, 'index.html')
