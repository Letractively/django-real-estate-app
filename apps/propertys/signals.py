import django.dispatch

property_viewed = django.dispatch.Signal(providing_args=["property","user", "request", "response"])