import os


def send_mail_with_images(message):
    from BeautifulSoup import BeautifulSoup
    from django.conf import settings
    import os

    s = BeautifulSoup(message.message_html)

    images = []
    imgs = s.findAll('img')
    image_index = 1
    for img in imgs:
        picfile = img['src']
        #        picfile = os.path.join( settings.MEDIA_ROOT, picfile.lstrip('/media/') )
        cid = 'image%d' % image_index
        img['src'] = 'cid:' + cid
        images.append((cid, picfile))
        image_index += 1

    html = unicode(s)
    send_html_mail(message.from_address,
                   message.to_address,
                   message.subject,
                   message.message_text,
                   html,
                   images)


def send_html_mail( from_email, to_email, subject, txt, html, images):
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.MIMEImage import MIMEImage
    from email.header import Header
    from django.conf import settings
    import smtplib

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = Header(subject.encode('utf-8'), 'utf-8')
    msgRoot['From'] = from_email
    msgRoot['To'] = to_email
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText(txt.encode('utf-8'), 'plain', 'utf-8')
    #    msgText.add_header('Content-Type', 'text/plain; charset="utf8"')
    msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
    #msgText.add_header('Content-Type', 'text/html; charset="utf8"')
    msgAlternative.attach(msgText)

    for cid, fname in images:

        fname = fname[1:] if fname[0] == '/' else fname
        data = open(os.path.join(settings.WORK_DIR, fname)).read()
        msgImage = MIMEImage(data)
        msgImage.add_header('Content-ID', '<%s>' % cid)
        msgRoot.attach(msgImage)


    # Send the email (this example assumes SMTP authentication is required)
    smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)

    if settings.EMAIL_USE_TLS:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

    if settings.EMAIL_HOST_USER:
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    smtp.sendmail(from_email, to_email, msgRoot.as_string())
    smtp.quit()