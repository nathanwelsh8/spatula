import re

# detect mobile devices and allow django to service custom mobile views
# source:https://stackoverflow.com/questions/42273319/detect-mobile-devices-with-django-and-python-3
def is_mobile(request):
    """Return True if the request comes from a mobile device."""

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

def screen_size(request):
    """Return sreensixe if it can be found """
    SCREEN_SIZE = re.compile(r"([0-9]{3})x([0-9]{3})", re.IGNORECASE)
    if SCREEN_SIZE.match(request.META['HTTP_USER_AGENT']):
        print("OUTPUT:",SCREEN_SIZE.match(request.META['HTTP_USER_AGENT']))
