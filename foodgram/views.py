from django.shortcuts import render


def page_not_found(request, exception): # noqa
    return render(
        request,
        'users/message_page.html',
        {'message': 'Ошибка 404'},
        status=404
    )


def server_error(request):
    return render(
        request,
        'users/message_page.html',
        {'message': 'ошибка 500'},
        status=500
    )
