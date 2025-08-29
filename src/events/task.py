from celery import shared_task

from .models import Registration


@shared_task
def async_registration_for_event(registration_id):
    reg = Registration.objects.get(id=registration_id)
    #     тут запрос на регистрацию в евент провайдер

    send_registration_notification.delay(reg.id)


@shared_task
def send_registration_notification(registration_id):
    reg = Registration.objects.get(pk=registration_id)
    #     отправляем
    reg.notification_send = True
    reg.save()
