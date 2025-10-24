# from django.core.mail import send_mail
# from django.conf import settings

# def send_book_notification_email(user_email, book_title, status, message):
#     subject = f"📚 Book Available: {book_title}"
    
#     if status == "reserved":
#         message = f"The book '{book_title}' is now available for you to borrow. You are first in line as a reserved user. Please borrow it within 5 days."
#     elif status == "waiting":
#         message = f"The book '{book_title}' is now available and you’ve been promoted from waiting to reserved. Please check your dashboard and borrow it soon."

#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [user_email],
#         fail_silently=False,
#     )


from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import IssuedBook
from datetime import timedelta

def send_book_notification_email(user_email, subject, message):
    """
    Sends an email with a custom subject and message.
    """
    if not message:
        print("❌ Email message is empty. Not sending.")
        return
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )


def send_expiry_reminders():
    today = timezone.now().date()

    # Get issued books that will expire tomorrow
    issued_books = IssuedBook.objects.filter(expiry_date=today + timedelta(days=1))

    for issued_book in issued_books:
        student = issued_book.student
        if student.email:  # make sure email exists
            send_mail(
                subject="Library Book Return Reminder",
                message=f"Dear {student.username},\n\nThis is a reminder that your borrowed book '{issued_book.book.name}' is due tomorrow ({issued_book.expiry_date}). Please return it on time to avoid fines.",
                from_email="pprathisha4@gmail.com",
                recipient_list=[student.email],
                fail_silently=True,
            )