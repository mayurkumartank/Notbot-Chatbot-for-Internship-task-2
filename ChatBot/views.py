from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
import datetime

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        print(request.POST)
        body = request.POST['Body'].strip().lower()
        twilio_phone_number = request.POST['To']
        recipient_phone_number = request.POST['From']
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message_body = ""
        if body.startswith('remind me at '):
            reminder_time_str = body.replace('remind me at ', '')
            try:
                reminder_time = datetime.datetime.strptime(reminder_time_str, '%Y-%m-%d %H:%M')
                current_time = datetime.datetime.now()

                if reminder_time > current_time:
                    time_delay = (reminder_time - current_time).total_seconds()

                    schedule_reminder(twilio_phone_number, recipient_phone_number, f"Your appointment is coming up on {reminder_time}", time_delay)

                    message_body += f"Reminder scheduled for {reminder_time}."
                else:
                    message_body += "Please Valid date and time enter"
            except ValueError:
                message_body += "Invalid date and time format. Please use 'YYYY-MM-DD HH:MM'."
        elif body == 'hello':
            message_body += "Hello, how can I help you?"
        elif body == 'bye':
            message_body += "Goodbye! Have a great day."
        elif body == 'ok' or body == 'okay':
            message_body += "Okay, feel free to reach out if you need any assistance."
        else:
            message_body += "Sorry, I don't understand that."

        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )

        return HttpResponse(f"Message sent successfully: {message.sid}")
    else:
        return HttpResponse("This endpoint only accepts POST requests.")

def schedule_reminder(sender_phone_number, recipient_phone_number, message_data, time_delay):
    import threading

    def send_reminder():
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_data,
            from_=sender_phone_number,
            to=recipient_phone_number
        )

    reminder_thread = threading.Timer(time_delay, send_reminder)
    reminder_thread.start()
