from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, StudentQuery, CourseNew, Department ,Holiday,LibrarySetting,IssuedBook, StudentExtra, Genre, FooterContent


class FooterContentForm(forms.ModelForm):
    class Meta:
        model = FooterContent
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(FooterContentForm, self).__init__(*args, **kwargs)
        self.fields['about'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Write something about the footer...',
            'rows': 4,
            'style': 'resize: vertical;'
        })

class BrandingForm(forms.ModelForm):
    class Meta:
        model = LibrarySetting
        fields = ['brand_name', 'logo']

class ExpiryFineForm(forms.ModelForm):
    class Meta:
        model = LibrarySetting
        fields = ['expiry_days', 'fine_per_day']

class AdminCredentialForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, user):
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password'])
        user.save()
        


class CourseDepartmentForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=CourseNew.objects.all(),
        empty_label="Select Course",
        required=False
    )
    department = forms.CharField(max_length=100, required=False, label="Department Name")
    new_course = forms.CharField(max_length=100,required=False, label="New Course")

    def clean_new_course(self):
        new_course_name = self.cleaned_data.get("new_course")
        if new_course_name:
            exists = CourseNew.objects.filter(name__iexact=new_course_name).exists()
            if exists:
                raise forms.ValidationError(f"⚠️ The course '{new_course_name}' already exists.")
        return new_course_name

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'course']

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentExtra


class StudentSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile_number = forms.CharField(max_length=15, required=True, label="Mobile Number")
    roll_number = forms.CharField(max_length=50, required=True, label="Roll Number")
    course = forms.ModelChoiceField(queryset=None, required=False, empty_label="Select Course", label="Course")  # set in __init__
    department = forms.ModelChoiceField(queryset=None, required=False, empty_label="Select Department", label="Department")  # set in __init__
    year = forms.ChoiceField(choices=StudentExtra.YEAR_CHOICES, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2",
                  "mobile_number", "roll_number", "course", "department", "year"]
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'returned_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        from .models import CourseNew, Department
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = CourseNew.objects.all()
        self.fields['department'].queryset = Department.objects.all()

    def save(self, commit=True):
        # Save User first
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        # Create linked StudentExtra
        student = StudentExtra(
            user=user,
            mobile_number=self.cleaned_data['mobile_number'],
            roll_number=self.cleaned_data['roll_number'],
            course=self.cleaned_data.get('course'),
            department=self.cleaned_data.get('department'),
            year=self.cleaned_data['year']
        )
        if commit:
            student.save()

        return user



class EditStudentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class EditStudentExtraForm(forms.ModelForm):
    class Meta:
        model = StudentExtra
        fields = ['mobile_number','course', 'department', 'year', 'roll_number']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control','id': 'id_course'}),
            'department': forms.Select(attrs={'class': 'form-control','id': 'id_department'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(EditStudentExtraForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'isbn', 'quantity', 'genre', 'image', 'description', 'published_date','bestseller','newly_published','language', 'publisher','price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Name'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN-13'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Book description', 'rows': 4}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'published_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bestseller': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'newly_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Publisher'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'step': '0.01', 'min': '0'}),
        }

class IssueBookForm(forms.Form):
    # Student Info
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'readonly': True}))
    mobile_number = forms.CharField(label='Mobile Number', max_length=15, widget=forms.TextInput(attrs={'readonly': True}))
    roll_number = forms.CharField(label='Roll Number', max_length=20, widget=forms.TextInput(attrs={'readonly': True}))

    # Book Info
    book_unique_id = forms.CharField(label='Book Unique ID', max_length=50, widget=forms.TextInput(attrs={'readonly': True}))
    book_title = forms.CharField(label='Book Title', max_length=200, widget=forms.TextInput(attrs={'readonly': True}))
    isbn = forms.CharField(label='ISBN', max_length=20, widget=forms.TextInput(attrs={'readonly': True}))
    genre = forms.CharField(label='Genre', max_length=100, widget=forms.TextInput(attrs={'readonly': True}))
    language = forms.CharField(label='Language', max_length=50, widget=forms.TextInput(attrs={'readonly': True}))
    
    #  admin fields
    fine = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'id': 'id_fine'}))
    custom_expiry_days = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'id': 'id_custom_expiry_days'}))
    
    # Hidden Fields for actual foreign key IDs
    student_id = forms.IntegerField(widget=forms.HiddenInput())
    book_id = forms.IntegerField(widget=forms.HiddenInput())

   
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'image']

class StudentQueryForm(forms.ModelForm):
    class Meta:
        model = StudentQuery
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write your query here...',
                'rows': 4
            })
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = StudentQuery
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your reply here...'}),
        }

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'placeholder': 'e.g., Diwali, Sunday, Govt Holiday'})
        }