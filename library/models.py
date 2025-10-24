from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta, date
from django.utils import timezone
from django.utils.timezone import now
import random
import io
from io import BytesIO
from django.conf import settings
import qrcode
import barcode
from django.core.files.base import ContentFile
from barcode import Code128
from barcode.writer import ImageWriter
from django.core.files import File
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from decimal import Decimal


class FooterContent(models.Model):
    
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    about = models.TextField(max_length=500)
    working_hours = models.CharField(max_length=100)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    google = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    def __str__(self):
        return "Footer Content"
    
def generate_barcode_image(barcode_id: str) -> bytes:
    code = Code128(barcode_id, writer=ImageWriter())
    buffer = io.BytesIO()

    code.write(
        buffer,
        {
            "write_text": True,
            "font_size": 10,
            "text_distance": 5,
            "module_width": 0.3,
            "module_height": 30,
        }
    )
    return buffer.getvalue()


class CourseNew(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

class Department(models.Model):
    course = models.ForeignKey(CourseNew, on_delete=models.CASCADE, null=True, related_name="departments")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('course', 'name')  # Prevent duplicates for same course

    def __str__(self):
        return f"{self.name} ({self.course.name})"


class StudentExtra(models.Model):
   
    YEAR_CHOICES = [
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
    ]
   
   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseNew, on_delete=models.SET_NULL, null=True, blank=True)
    is_student = models.BooleanField(default=True)
    email = models.EmailField(blank=True, null=True) 
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, default='1st')
    roll_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=15)
    barcode = models.ImageField(upload_to="barcodes/", null=True, blank=True)
    barcode_id = models.CharField(max_length=30, unique=True, null=True, blank=True)
  
       
   


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new or not self.barcode_id:
            self.barcode_id = f"S{self.pk:05d}"  # e.g., S00012

        # Only regenerate if barcode image is missing
        if not self.barcode:
            barcode_image = generate_barcode_image(self.barcode_id)
            filename = f"student_{self.pk}.png"
            self.barcode.save(filename, ContentFile(barcode_image), save=False)

        super().save(update_fields=["barcode", "barcode_id"])

    def __str__(self):
        return self.user.username

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def email(self):
        return self.user.email

    @property
    def getuserid(self):
        return self.user.id
  


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='genre_images/')

    def __str__(self):
        return self.name
    
class Notification(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

# language in book model
LANGUAGE_CHOICES = [
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('Tamil', 'Tamil'),
    ('Malayalam', 'Malayalam'),
    ('Telugu', 'Telugu'),
    ('Kannada', 'Kannada'),
    ('Bengali', 'Bengali'),
    ('Other', 'Other'),
]

def _qr_png_from_text(text: str) -> bytes:
    img = qrcode.make(text)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

class Book(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    copy_number = models.PositiveIntegerField(default=1)  # new field
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # ✅ For penalty
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)
    bestseller = models.BooleanField(default=False)
    newly_published = models.BooleanField(default=False)
    published_date = models.DateField(null=True, blank=True)
    donated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='donated_books')
    is_donated = models.BooleanField(default=False)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, default='English')
    publisher = models.CharField(max_length=100, blank=True, null=True)
    qrcode = models.ImageField(upload_to="qrcodes/", null=True, blank=True)
    qrcode_value = models.CharField(max_length=500, db_index=True, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    book_unique_id = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.copy_number:  # only for new objects
            last_copy = Book.objects.filter(isbn=self.isbn).order_by('-copy_number').first()
            self.copy_number = (last_copy.copy_number + 1) if last_copy else 1

        if not self.book_unique_id:
            last_book = Book.objects.order_by('-id').first()
            if last_book and last_book.book_unique_id:
                last_id = int(last_book.book_unique_id.replace('LIB', ''))
                self.book_unique_id = f"LIB{last_id+1:03d}"
            else:
                self.book_unique_id = "LIB001"

        super().save(*args, **kwargs)

        # QR code generation
        qr_text = f"BOOK|{self.id}|{self.book_unique_id}|{self.name}|{self.genre.name}|{self.language}|{self.isbn}|{self.copy_number}"
        if self.qrcode_value != qr_text or not self.qrcode:
            self.qrcode_value = qr_text
            qr_png = _qr_png_from_text(qr_text)
            filename = f"book_{self.book_unique_id}_{self.copy_number}.png"
            self.qrcode.save(filename, ContentFile(qr_png), save=False)

            super().save(update_fields=["qrcode", "qrcode_value"])

   
    def is_recent(self):
        if self.newly_published and self.published_date:
            return (timezone.now().date() - self.published_date).days <= 30
        return False

    class Meta:
        unique_together = ('isbn', 'copy_number') 

    def __str__(self):
        return f"{self.name} (Copy {self.copy_number}, ID: {self.book_unique_id})"
    
    
class LibrarySetting(models.Model):
    brand_name = models.CharField(max_length=255, default='My Library', blank=True, null=True)
    logo = models.ImageField(upload_to='library_logo/', blank=True, null=True)
    expiry_days = models.PositiveIntegerField(default=7)
    fine_per_day = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return self.brand_name
    
    def save(self, *args, **kwargs):
        self.pk = 1  # ensure singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Library Global Settings"

class Holiday(models.Model):
    date = models.DateField(unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.description or 'Holiday'}"



def get_expiry():
    settings = LibrarySetting.get_settings()
    return date.today() + timedelta(days=settings.expiry_days)

class IssuedBook(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    expiry_date = models.DateField()
    issued_date = models.DateField(default=timezone.now)
    requested_date = models.DateTimeField(default=now)
    returned = models.BooleanField(default=False)
    returned_date = models.DateField(default=timezone.now) 
    STATUS_CHOICES = [
    ('Borrowed', 'Borrowed'),
    ('Reserved', 'Reserved'),
    ('Waiting', 'Waiting'),
    ('Returned', 'Returned'),
    ('Missing', 'Missing'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Borrowed')
    payment_method = models.CharField(max_length=50, blank=True, null=True)  # 'Cash' or 'GPay'
    fine_per_day = models.PositiveIntegerField(default=10)  # Admin-settable fine
    final_fine = models.IntegerField(default=0)  # This will store the fine when returned
    canceled = models.BooleanField(default=False)
    canceled_by = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin')], null=True, blank=True)
    custom_expiry_days = models.PositiveIntegerField(default=7, null=True, blank=True)  # Admin-settable days
    renewed = models.BooleanField(default=False)  # one-time renewal flag
    missing = models.BooleanField(default=False)   # ✅ Missing book
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    fine_cancelled = models.BooleanField(default=False)   # ✅ New field
    fine_cancel_reason = models.CharField(max_length=255, blank=True, null=True)  # e.g., Holiday, Sunday
 
    def calculate_fine(self) -> int:
        """Overdue fine up to today (if not returned), excluding holidays and Sundays."""
        if not self.returned and self.expiry_date and date.today() > self.expiry_date:
            holidays = set(Holiday.objects.values_list('date', flat=True))

            fine_days = 0
            current_date = self.expiry_date + timedelta(days=1)
            today = date.today()

            while current_date <= today:
                # Skip Sundays (weekday() == 6) and listed holidays
                if current_date.weekday() != 6 and current_date not in holidays:
                    fine_days += 1
                current_date += timedelta(days=1)

            return fine_days * int(self.fine_per_day)
        return 0

    def calculate_missing_penalty(self) -> Decimal:
        
        base = Decimal(getattr(self.book, "price", 0))
        late = Decimal(self.calculate_fine())
        return base + late

    def save(self, *args, **kwargs):
        settings = LibrarySetting.get_settings()

        # Apply fine_per_day from settings if caller left default in place
        if not self.fine_per_day or self.fine_per_day == 10:
            self.fine_per_day = settings.fine_per_day

        # Set expiry_date if missing
        if not self.expiry_date:
            expiry_days = self.custom_expiry_days or settings.expiry_days
            self.expiry_date = (self.issued_date or date.today()) + timedelta(days=expiry_days)

        # Final fine logic:
        if self.missing:
            # 👇 no settings.missing_fine — use book.price + late fine
            self.final_fine = int(self.calculate_missing_penalty())
            self.status = 'Missing'
        elif self.returned and self.final_fine == 0:
            # Charge overdue fine only if book is actually late
            self.final_fine = self.calculate_fine()

        super().save(*args, **kwargs)

    def get_display_fine(self) -> str:
        if self.missing:
            return f"₹{self.final_fine}" if self.final_fine > 0 else "Missing Fine Pending"
        # if self.fine_cancelled and self.fine_cancel_reason:
        #     return f"No Fine ({self.fine_cancel_reason})"
        if self.fine_cancelled and self.fine_cancel_reason:
            return f"₹{self.final_fine}" if self.final_fine > 0 else "No Fine"
        if self.returned:
            return f"₹{self.final_fine}" if self.final_fine > 0 else "No Fine"
        if self.expiry_date and date.today() > self.expiry_date:
            return f"₹{self.calculate_fine()}"
        return "No Fine"


    @property
    def waiting_days_left(self):
        # from datetime import datetime, timedelta

        position = self.queue_position()  # Assume this is already defined
        expiry_days = self.custom_expiry_days if self.custom_expiry_days is not None else 7  # Default to 7

        assigned_days = (position + 1) * expiry_days
        if self.issued_date:
            end_date = self.issued_date + timedelta(days=assigned_days)
            return (end_date - datetime.now().date()).days
        return None

    
    def queue_position(self):
        """
        Return 0 for reserved user, 1 for first waiting user, 2 for second, etc.
        """
        if self.status in ['Reserved', 'Waiting']:
            others = IssuedBook.objects.filter(
                book=self.book,
                status__in=['Reserved', 'Waiting'],
                returned=False
            ).order_by('issued_date', 'id')

            for index, record in enumerate(others):
                if record.id == self.id:
                    return index
        return -1
 
    @property
    def book_available(self):
        # Only the first waiting user (position 0) should get "Available Now!"
        return self.book.quantity > 0 and self.queue_position() == 0
    def __str__(self):
        return f"Issued: {self.book.name} to {self.student.username}"

class BookRequestQueue(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"Waiting: {self.book.name} by {self.student.username}"
    
class StudentQuery(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    reply = models.TextField(blank=True, null=True)
    # replied_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Query by {self.student.username} at {self.submitted_at}"
