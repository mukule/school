from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import DateInput
from django.forms import ModelForm, DateInput
from .models import *




class UserRegisterForm(UserCreationForm):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'ID NUMBER', 'class': 'form-control'}),
        label='',
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        label='',
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'class': 'form-control'}),
        label='',
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'class': 'form-control'}),
        label='',
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control', 'autocomplete': 'new-password'}),
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='User Type',
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'Date of Birth', 'class': 'form-control'}),
        label='',
        required=False,
    )
    contact_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Contact Number', 'class': 'form-control'}),
        label='',
        required=False,
    )
    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
        label='',
        required=False,
    )
    parent_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Parent Name', 'class': 'form-control'}),
        label='',
        required=False,
    )
    parent_contact = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Parent Contact', 'class': 'form-control'}),
        label='',
        required=False,
    )
    class_admitted = forms.ModelChoiceField(
        queryset=ClassName.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Class Admitted',
        required=False,
    )
    current_class = forms.ModelChoiceField(
        queryset=ClassName.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Current Class',
        required=False,
    )
    entry_marks = forms.FloatField(
        widget=forms.NumberInput(attrs={'placeholder': 'Entry Marks', 'class': 'form-control'}),
        label='',
        required=False,
    )
    date_of_admission = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'Date of Admission', 'class': 'form-control'}),
        label='',
        required=False,
    )
    house = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'House', 'class': 'form-control'}),
        label='',
        required=False,
    )
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Subjects',
        required=False,
    )
    curriculum_activity = forms.ModelChoiceField(
        queryset=CurriculumActivity.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Curriculum Activity',
        required=False,
    )
    leadership = forms.ModelChoiceField(
        queryset=Leadership.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Leadership',
        required=False,
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type', 'date_of_birth', 'contact_number', 'address', 'parent_name', 'parent_contact', 'class_admitted', 'current_class', 'entry_marks', 'date_of_admission', 'house', 'subjects', 'curriculum_activity', 'leadership']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user
    
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Admin/Student ID'}),
        label="")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
class TeacherCreationForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]


    national_id = forms.CharField(
        max_length=20,
        label='National ID',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        max_length=50,
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label='Gender',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=20,
        label='Phone Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        max_length=100,
        label='Address',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    subjects_taught = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        label='Subjects Taught',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    classes_taught = forms.ModelMultipleChoiceField(
        queryset=ClassName.objects.all(),
        label='Classes Taught',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    qualifications = forms.CharField(
        label='Qualifications',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    experience = forms.IntegerField(
        label='Experience',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    employment_status = forms.CharField(
        max_length=20,
        label='Employment Status',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nationality = forms.CharField(
        max_length=50,
        label='Nationality',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    interests = forms.CharField(
        label='Interests',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    emergency_contact_name = forms.CharField(
        max_length=100,
        label='Emergency Contact Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    emergency_contact_number = forms.CharField(
        max_length=20,
        label='Emergency Contact Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    photo = forms.ImageField(
        label='Photo',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        label='Notes',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    curriculum_activities = forms.ModelMultipleChoiceField(
        queryset=CurriculumActivity.objects.all(),
        label='Curriculum Activities',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
   
    class Meta:
        model = Teacher
        fields = '__all__'

    def save(self, commit=True):
        teacher = super().save(commit=False)

        if commit:
            teacher.save()

        self.save_m2m()
        return teacher
