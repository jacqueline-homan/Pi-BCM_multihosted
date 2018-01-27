def flash(request, message, category):
    try:
        request.session['flash_messages'].append((message, category),)
    except KeyError:
        request.session['flash_messages'] = []
        request.session['flash_messages'].append((message, category), )


def flash_get_messages(request):
    flashed_messages = request.session.get('flash_messages', [])
    request.session['flash_messages'] = []
    return flashed_messages


def flash_test(request):
    flash(request, 'Test message 1', 'success')
    flash(request, 'Test message 2', 'warning')
    flashed_messages = flash_get_messages(request)
    flashed_messages = flash_get_messages(request)
    pass
