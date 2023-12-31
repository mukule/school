from django.contrib.auth.views import LoginView
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.views.generic import *
from django.http import JsonResponse
from django.db.models import Count


def get_filtered_streams(request):
    class_id = request.GET.get('class_id')
    streams = Stream.objects.filter(class_name_id=class_id).values('id', 'name')
    return JsonResponse({'streams': list(streams)})

# @user_passes_test(lambda u: u.is_authenticated and u.user_type == 'admin', login_url='users:login')
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.user_type == 'student':
                # Assign house and stream to the student
                houses = House.objects.annotate(student_count=Count('students')).order_by('student_count', 'capacity')
                house = houses.filter(student_count__lt=models.F('capacity')).first()
                stream = Stream.objects.filter(class_name=user.class_admitted).annotate(student_count=Count('students')).order_by('student_count').first()
                if house and stream:
                    user.house = house
                    user.stream = stream
                    house.student_count += 1
                    house.save()
                else:
                    messages.error(request, 'Cannot assign house or stream. Please try again later.')
            user.save()
            messages.success(request, f'User {user.username} has been created successfully.')
            return redirect('main:dashboard_admin')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = UserRegisterForm()

    return render(request, 'adminstrator/create_student.html', {'form': form})

def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                auth_login(request, user)
                if user.user_type == 'student':
                    return redirect("main:dashboard")
                elif user.user_type == 'admin':
                    return redirect("main:dashboard_admin")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="users/index.html",
        context={"form": form}
    )


def custom_logout(request):
    logout(request)
    messages.info(request, "succesfully logged out")
    return redirect("users:login")
    
@login_required
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, 'Teacher created successfully.')
            return redirect('users:teachers')  # Redirect to the TeacherListView
    else:
        form = TeacherCreationForm()

    return render(request, 'adminstrator/create_teacher.html', {'form': form})

class teachers(ListView):
    model = Teacher
    template_name = 'adminstrator/teachers.html'
    context_object_name = 'teachers'

def student(request):
    User = get_user_model()
    students = User.objects.filter(user_type='student')

    return render(request, 'adminstrator/student.html', {'students': students})

def create_parent(request):
    if request.method == 'POST':
        form = ParentCreationForm(request.POST)
        if form.is_valid():
            parent = form.save(commit=False)
            parent.user = request.user  # Assign the current user as the parent's user
            parent.save()
            form.save_m2m()  # Save the many-to-many relationships, if any
            messages.success(request, 'Parent created successfully.')
            return redirect('users:parents')  # Redirect to parent list page
        else:
            messages.error(request, 'Error creating parent. Please check the form.')
    else:
        form = ParentCreationForm()
    
    return render(request, 'adminstrator/create_parent.html', {'form': form})

def parents(request):
    parents = Parent.objects.all()
    return render(request, 'adminstrator/parents.html', {'parents': parents})

def classes(request):
    classes = ClassName.objects.all()
    return render(request, 'adminstrator/classes.html', {'classes': classes})

def class_detail(request, class_id):
    class_obj = get_object_or_404(ClassName, id=class_id)
    # Add any additional data you want to pass to the template
    context = {
        'class_obj': class_obj,
    }
    return render(request, 'adminstrator/class_details.html', context)

def stream_detail(request, stream_id):
    stream = get_object_or_404(Stream, id=stream_id)
    exams = Exam.objects.all()

    context = {
        'stream': stream,
        'exams': exams,
    }
    
    return render(request, 'adminstrator/stream_detail.html', context)



def subject_selection_view(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)

    if request.method == 'POST':
        form = SubjectSelectionForm(request.POST, subjects=Subject.objects.all())
        if form.is_valid():
            selected_subjects = form.cleaned_data['subjects']

            for subject in selected_subjects:
                student_subject, created = StudentSubject.objects.get_or_create(student=student, subject=subject)
                student_subject.marks = 0.0
                student_subject.save()

            stream_id = student.stream.id  # Get the stream_id from the student object

            # Add success message
            messages.success(request, f"Subjects selected successfully for {student.get_full_name()}")

            return redirect('users:stream_detail', stream_id=stream_id)
    else:
        form = SubjectSelectionForm(subjects=Subject.objects.all())

    context = {
        'form': form,
        'student': student
    }

    return render(request, 'adminstrator/subject_selection.html', context)

def update_subjects(request, student_id, exam_id):
    student = get_object_or_404(CustomUser, id=student_id)
    exam = get_object_or_404(Exam, id=exam_id)
    student_subjects = student.subjects.all()

    if request.method == 'POST':
        form = SubjectMarksForm(request.POST, subjects=student_subjects)

        if form.is_valid():
            for student_subject in student_subjects:
                marks = form.cleaned_data[f'marks_{student_subject.id}']
                
                result, _ = Result.objects.update_or_create(
                    student_subject=student_subject,
                    exam=exam,
                    defaults={'marks': marks}
                )

            messages.success(request, "Subject marks updated successfully.")
            return redirect('users:student_result', student_id=student_id, exam_id=exam_id)
        else:
            # Display form errors as messages
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
    else:
        initial_data = {}
        for student_subject in student_subjects:
            result = Result.objects.filter(
                student_subject=student_subject,
                exam=exam
            ).first()
            marks = result.marks if result else Decimal('0.00')
            initial_data[f'marks_{student_subject.id}'] = marks

        form = SubjectMarksForm(subjects=student_subjects, initial=initial_data)

    # Add form errors to the form fields
    for field in form:
        if field.errors:
            field_class = field.field.widget.attrs.get('class', '')
            field.field.widget.attrs['class'] = f'{field_class} is-invalid'

    context = {
        'student': student,
        'exam': exam,
        'subjects': student_subjects,
        'form': form,
    }

    return render(request, 'adminstrator/update_subject_marks.html', context)



def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            # Perform any additional actions after saving the exam
            return redirect('users:exams')
    else:
        form = ExamForm()
    return render(request, 'adminstrator/create_exam.html', {'form': form})

def exams(request):
    exams = Exam.objects.all()
    return render(request, 'adminstrator/exams.html', {'exams': exams})


def exam_result(request, exam_id, stream_id):
    exam = get_object_or_404(Exam, id=exam_id)
    class_name = exam.classes.first()  # Assuming each exam is associated with a class
    stream = get_object_or_404(Stream, id=stream_id, class_name=class_name)

    # Retrieve all the students from the stream within the class
    students = stream.students.all()

    # Retrieve the results for the given exam and students
    results = Result.objects.filter(exam=exam, student_subject__student__in=students)
  

    # Create a dictionary to map student IDs to their corresponding results
    student_results = {}
    for result in results:
        student_id = result.student_subject.student.id
        if student_id not in student_results:
            student_results[student_id] = []
        student_results[student_id].append(result)
        print(student_results)

    context = {
        'exam': exam,
        'students': students,
        'student_results': student_results,
    }

    return render(request, 'adminstrator/exam_result.html', context)

def update_subject_marks(request, student_id, exam_id):
    student = get_object_or_404(CustomUser, id=student_id)
    exam = get_object_or_404(Exam, id=exam_id)
    student_subjects = student.subjects.all()

    if request.method == 'POST':
        form = SubjectMarksForm(request.POST, subjects=student_subjects)

        if form.is_valid():
            marks_data = {}
            for student_subject in student_subjects:
                marks = form.cleaned_data[f'marks_{student_subject.id}']
                marks_data[student_subject.id] = marks

            comment = form.cleaned_data['comment']

            for student_subject in student_subjects:
                marks = marks_data[student_subject.id]
                result, _ = Result.objects.update_or_create(
                    student_subject=student_subject,
                    exam=exam,
                    defaults={'marks': marks}
                )

            # Update the teacher comment for all subjects
            Result.objects.filter(student_subject__in=student_subjects, exam=exam).update(
                teacher_comments=comment
            )

            messages.success(request, "Subject marks and comment updated successfully.")
            return redirect('users:student_result', student_id=student_id, exam_id=exam_id)
        else:
            # Display form errors as messages
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
    else:
        initial_data = {}
        for student_subject in student_subjects:
            result = Result.objects.filter(
                student_subject=student_subject,
                exam=exam
            ).first()
            marks = result.marks if result else Decimal('0.00')
            initial_data[f'marks_{student_subject.id}'] = marks

        # Get the existing teacher comment
        comment = Result.objects.filter(student_subject__in=student_subjects, exam=exam).first()
        comment_initial = comment.teacher_comments if comment else 'No comment'
        initial_data['comment'] = comment_initial

        form = SubjectMarksForm(subjects=student_subjects, initial=initial_data)

    # Add form errors to the form fields
    for field in form:
        if field.errors:
            field_class = field.field.widget.attrs.get('class', '')
            field.field.widget.attrs['class'] = f'{field_class} is-invalid'

    context = {
        'student': student,
        'exam': exam,
        'subjects': student_subjects,
        'form': form,
    }

    return render(request, 'adminstrator/update_subject_marks.html', context)


def view_student_results(request, student_id, exam_id):
    student = get_object_or_404(CustomUser, id=student_id, user_type='student')
    exam = get_object_or_404(Exam, id=exam_id)
    print(student_id, exam_id)
    # Retrieve the results for the student and exam
    results = Result.objects.filter(student_subject__student=student, exam=exam)

    # Debug statement to print mean grade
   
    context = {
        'student': student,
        'exam': exam,
        'results': results,
    }

    return render(request, 'adminstrator/student_result.html', context)
