import django.dispatch

proprety_viewed = django.dispatch.Signal(providing_args=["porprety","user", "request", "response"])