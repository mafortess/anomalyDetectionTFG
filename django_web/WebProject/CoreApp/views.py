from django.shortcuts import render


def index(request):
    return render(request, 'CoreApp/index.html', context)

def help(request):
    return render(request, 'CoreApp/help.html', {})


#from django.http import HttpResponse

#def index(request):
#    return HttpResponse("MENHello, world. You're at the monitor index.")