from django.core import mail
from django.core.mail.message import EmailMessage

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from django.db import models
from django.db.models.signals import post_save

from django.template.loader import render_to_string

from ab_site.models import Customer


class Article(models.Model):
    text = models.TextField(verbose_name='Body of the article')
    created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    sending = models.BooleanField(default=False, verbose_name='Send',
                                  help_text='Send this article via maillist to subscribers')
    sent = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'News'

    def __unicode__(self):
        return self.text


def send_maillist(sender, instance, created, *args, **kwargs):
    article = instance
    if article.sending and not article.sent:
        subscribers = Customer.objects.filter(is_subscribed=True)
        messages = []
        from_email = u"{name} <{email}>".format(name=article.author.get_full_name(), email=article.author.email).strip()
        domain_name = Site.objects.get_current().domain
        for subscriber in subscribers:
            message_context = {'article': article,
                               'email': subscriber,
                               'domain': domain_name}
            message_text = render_to_string('maillist_text.txt', message_context)
            email = EmailMessage('Breaking news!', message_text,
                                 from_email=from_email, to=[subscriber.email])
            email.content_subtype = 'html'
            messages.append(email)
        connection = mail.get_connection()
        connection.send_messages(messages)
        connection.close()
        article.sent = True
        article.save()


# post_save.connect(send_maillist, sender=Article)