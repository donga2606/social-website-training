from django.shortcuts import get_object_or_404, redirect, render, HttpResponse


def home(request):
    user = request.user
    hello = 'hello world'
    context = {
        'user': user,
        'hello': hello,
    }
    return render(request, 'main/home.html', context)
