from django.shortcuts import render


def about(request):
    message = 'автор еще не придумал, что он хочет рассказать о себе'
    return render(request, 'users/message_page.html', {'message': message})


def technologies(request):
    message = 'stack: django + drf + python'
    return render(request, 'users/message_page.html', {'message': message})
