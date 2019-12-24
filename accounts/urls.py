from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^login', 'accounts.views.log_in', name='login'),
    url(r'^logout', 'accounts.views.log_out'),
    url(r'^reset_password', 'accounts.views.reset_password', name="reset-password"),
    url(r'^reset_target', 'accounts.views.reset_target', name="reset-target"),
    url(r'^send_sms', 'accounts.views.send_sms', name="send-sms"),
    url(r'^registration/', 'accounts.views.pre_registration', name='pre-registration'),
    url(r'^person-registration/', 'accounts.views.person_registration', name='person-registration'),
    url(r'^company-registration/', 'accounts.views.company_registration', name='company-registration'),
    url(r'^registration-complete/', 'accounts.views.registration_complete', name='registration-complete'),
    url(r'^registration-confirm/(?P<key>\w+)/', 'accounts.views.registration_confirm', name='registration-confirm'),
)
