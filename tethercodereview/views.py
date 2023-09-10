from django.http import HttpResponse
import logging


logger = logging.getLogger("django")


def hello_world(request):
    # Logic for the view
    message = "Hello, World!"
    logger.warning("this is test message from warning")
    # Return the HTTP response
    return HttpResponse(message)
