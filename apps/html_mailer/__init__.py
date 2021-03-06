VERSION = (0, 1, 0, "alpha")

def get_version():
    if VERSION[3] != "final":
        return "%s.%s.%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3])
    else:
        return "%s.%s.%s" % (VERSION[0], VERSION[1], VERSION[2])

__version__ = get_version()

PRIORITY_MAPPING = {
    "high": "1",
    "medium": "2",
    "low": "3",
    "deferred": "4",
    "immediately": "5",
}

# replacement for django.core.mail.send_mail

def send_mail(subject, message, from_email, recipient_list, priority="medium",
              fail_silently=False, auth_user=None, auth_password=None):
    from django.utils.encoding import force_unicode
    from html_mailer.models import Message

    """ 
    Set up body params - to avoid backward-incompatible changes in the django-mailer
    interface, body can be passed as a dict if html mail is required. Otherwise, 
    body is just plain text and django-mailer will behave normally.
    """
    if type(message) == type(dict()):
        message_text = message['text']
        message_html = message['html']
    else:
        message_text = message
        message_html = None
    
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    priority = PRIORITY_MAPPING[priority]
    for to_address in recipient_list:
        m = Message(to_address=to_address,
                from_address=from_email,
                subject=subject,
                message_text=message_text,
                message_html=message_html,
                priority=priority)
        m.save()

def mail_admins(subject, message, fail_silently=False, priority="medium"):
    from django.utils.encoding import force_unicode
    from django.conf import settings
    from html_mailer.models import Message
    
    """ 
    Set up body params - to avoid backward-incompatible changes in the django-mailer
    interface, body can be passed as a dict if html mail is required. Otherwise, 
    body is just plain text and django-mailer will behave normally.
    """
    if type(message) == type(dict()):
        message_text = message['text']
        message_html = message['html']
    else:
        message_text = message
        message_html = '<pre>' + message + '</pre>'
        
    priority = PRIORITY_MAPPING[priority]
    for name, to_address in settings.ADMINS:
        Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                message_text=message_text,
                message_html=message_html,
                priority=priority).save()

def mail_managers(subject, message, fail_silently=False, priority="medium"):
    from django.utils.encoding import force_unicode
    from django.conf import settings
    from html_mailer.models import Message
    
    """ 
    Set up body params - to avoid backward-incompatible changes in the django-mailer
    interface, body can be passed as a dict if html mail is required. Otherwise, 
    body is just plain text and django-mailer will behave normally.
    """
    if type(message) == type(dict()):
        message_text = message['text']
        message_html = message['html']
    else:
        message_text = message
        message_html = None
        
    priority = PRIORITY_MAPPING[priority]
    for name, to_address in settings.MANAGERS:
        Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                message_text=message_text,
                message_html=message_html,
                priority=priority).save()
