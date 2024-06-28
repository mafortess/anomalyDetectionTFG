from django.shortcuts import render

def hostdash(request):
    return render(request, 'DashboardApp/HostDashboard.html', {})

def containerdash(request):
    return render(request, 'DashboardApp/ContainerDashboard.html', {})


def energytdash(request):
    return render(request, 'DashboardApp/EnergyTDashboard.html', {})
    
def aihostdash(request):
    return render(request, 'DashboardApp/AiHostDashboard.html', {})

def practdash(request):
    return render(request, 'DashboardApp/practdashboard.html', {})


