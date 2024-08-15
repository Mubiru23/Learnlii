from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import create_classForm ,create_subjectForm,create_lessonForm
#from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from . models import Lessons,Classes,Subjects
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .import forms
from .utils import send_email_notification


# sending email when a course is created

@login_required
def create_course(request):
    if not hasattr(request.user, 'teacher'):
        return redirect('home')

    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save()
            # Send email notification
            subject = 'New Marks Awarded'
            message = f'Dear {result.student.user.username},\n\nYou have been awarded {result.marks} marks for the {result.test or result.exam}.\n\nBest regards,\nYour School'
            recipient_list = [result.student.user.email]
            send_email_notification(subject, message, recipient_list)
            return redirect('teacher_results')
    else:
        form = ResultForm()
    return render(request, 'results/award_marks.html', {'form': form})



 
# create class view
def create_class(request): 
    submitted = False
    if request.method == 'POST':
        form = create_classForm(request.POST, request.FILES)
        if form.is_valid():
            classes=form.save(commit=False)
            classes.created_by = request.user
            classes.save()
            form.save() 
            # Send email notification
            #subject = 'New Course created'
            #message = f'Dear {classes.created_by.username},\n\n A new course {classes.title} has been created.\n\n you can sign into your learnli account and check for it. Good luck '
            #recipient_list = [classes.created_by.email]
            #send_email_notification(subject, message, recipient_list)
            return HttpResponseRedirect('/classes?submitted = True')

    else:
         form = create_classForm
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'create_class.html' ,{'form':form, 'submitted':submitted})

#Enroll into a course

def Enrolling(request, pk) :
     if request.user.is_authenticated:
        course = get_object_or_404(Classes, id = pk)
        is_enrolled = course.Enroll.filter(id=request.user.id).exists()
        #post form logic
        if request.method=='POST':
            if 'enroll' in request.POST and not is_enrolled:
                course.Enroll.add(request.user)
            if 'enroll' in request.POST and  is_enrolled:
                course.Enroll.remove(request.user)    
                return redirect('enroll', pk = pk)
            
        return render(request,'course_details.html',{
            'course':course,
             
            })   
     else: 
         messages.success(request,('you must be loged in to view this page'))
         return render(request, 'home.html')

# enrolled courses/ my_courses
def my_courses(request):
    my_courses = Classes.objects.all()
    return render(request,'my_courses.html',{
            'my_courses':my_courses,})
    



# create subject view
def create_subject(request): 
    submitted = False
    if request.method == 'POST':
        form = create_subjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject=form.save(commit=False)
            subject.taught_by = request.user
            subject.save()
            form.save() 
            return HttpResponseRedirect('/subjects?submitted = True')

    else:
         form = create_subjectForm
         if 'submitted' in request.GET:
             submitted = True
    return render(request,'create_subject.html' ,{'form':form, 'submitted':submitted})

   
# create lessons view
def create_lesson(request): 
    submitted = False
    if request.method == 'POST':
        form = create_lessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson=form.save(commit=False)
            lesson.taught_by = request.user
            lesson.position = request.user.id
            lesson.save()
            form.save() 
            return HttpResponseRedirect('/lessons?submitted = True')

    else:
         form = create_lessonForm
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'create_lesson.html' ,{'form':form, 'submitted':submitted}) 

#**** CREATING  VIEWS FOR CLASSES, SUBJECTS AND LESSONS***
# class view
def classes(request):
    classes = Classes.objects.all()
    return render(request,'classes.html',
    {
        'classes':classes
    })

# subject view
def subjects(request):
    subjects = Subjects.objects.all().order_by('-created_on')
    return render(request,'subjects.html',
    {
        'subjects':subjects
    })    

# lessons view
def lessons(request):
    lessons = Lessons.objects.all().order_by('-created_on')
    return render(request,'lessons.html',
    {
        'lessons':lessons
    }) 
#getsubjects for aparticular corse
def class_subjects(request,class_id):
    classes =get_object_or_404(Classes,id=class_id)
    subjects_for_class =classes.with_subjects.all()
    return render(request,'class_subjects.html',
    {
        'subjects_for_class':subjects_for_class
    
    })
# get lessons for aparticular subject
def subject_lessons(request,subject_id):
    subjects =get_object_or_404(Subjects,id=subject_id)
    lessons_for_subject =subjects.with_lessons.all()
    return render(request,'subject_lessons.html',
    {
        'lessons_for_subject':lessons_for_subject,
        'subjects':subjects,
    }) 

#**** EDITING CLASS, SUBJECTS AND LESSON CONTENT*****    
# Edit the class content

def edit_class(request, klass_id):
    klass = Classes.objects.get( pk = klass_id)
    form = create_classForm( request.POST or None, request.FILES or None, instance=klass)
    if form.is_valid():
           form.save()
           return redirect('classes')
    

    return render(request, 'edit_class.html', {
        "klass":klass,
        'form':form,
    })


# Edit the subject content
def edit_subject(request, subject_id):
    subject = Subjects.objects.get( pk = subject_id)
    form = create_subjectForm( request.POST or None, request.FILES or None, instance=subject)
    if form.is_valid():
           form.save()
           return redirect('subjects')
    

    return render(request, 'edit_subject.html', {
        "klass":subject,
        'form':form,
    })   


# Edit the lesson content
def edit_lesson(request, lesson_id):
    lesson = Lessons.objects.get( pk = lesson_id)
    form = create_lessonForm( request.POST or None, request.FILES or None, instance=lesson)
    if form.is_valid():
           form.save()
           return redirect('lessons')
    

    return render(request, 'edit_lesson.html', {
        "klass":lesson,
        'form':form,
    })  

 #*** DELETING A CLASS, LESSON OR SUBJECT***
 # Deleting a clas
def delete_class(request, klass_id):
    klass = Classes.objects.get( pk = klass_id)
    #if request.user == Classes. created_by:
    klass.delete()
    messages.success(request,('class Deleted!!'))
    return redirect('classes')
    #else:
         #messages.success(request,('you can not delete this class'))
         #return redirect('classes')

 #Deleting a subject
def delete_subject(request, subject_id):
    subject= Subjects.objects.get( pk = subject_id)
    #if request.user.user == Subjects.taught_by:
    subject.delete()
    messages.success(request,('subject Deleted!!'))
    return redirect('subjects')
    #else:
        # messages.success(request,('you can not delete this subject'))
        # return redirect('subjects')

 #Deleting a lesson
def delete_lesson(request, lesson_id):
    lesson= Lessons.objects.get( pk = lesson_id)
    #if request.user.user == Lessons. taught_by:
    lesson.delete()
    messages.success(request,('lesson Deleted!!'))
    return redirect('lessons')
    #else:
         #messages.success(request,('you can not delete this subject'))
         #return redirect('subjects')
