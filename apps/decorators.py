# -*- coding: utf-8 -*-


def get_client_ip(func):
    def wrap(request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        ip = None if ip == 'unknown' else ip
        return func(request, ip, *args, **kwargs)
    return wrap


