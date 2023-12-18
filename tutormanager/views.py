from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Tutor, Student, Feedback, Lesson, Schedule, AvailableSlot

import json, datetime

# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "tutormanager/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tutormanager/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        role = request.POST["role"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tutormanager/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if role == 'TUTOR':
                user = User.objects.create_user(username, email, password, role=1)
                
                try:
                    role = Group.objects.get(name='TUTOR')
                except:
                    role = Group.objects.create(name='TUTOR')
                
                user.groups.add(role)
                user.save()

                tutor = Tutor.objects.create(user=user)
                tutor.save()

            elif role == 'STUDENT':
                user = User.objects.create_user(username, email, password, role=2)

                try: 
                    role = Group.objects.get(name='STUDENT')
                except:
                    role = Group.objects.create(name='STUDENT')
                 
                user.groups.add(role)
                user.save()

                student = Student.objects.create(user=user)
                student.save()

        except IntegrityError:
            return render(request, "tutormanager/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "tutormanager/register.html")


def index(request):
    if request.user.is_authenticated:
        return render(request, "tutormanager/dashboard.html")
    else:
        return render(request, "tutormanager/login.html")



@login_required
def dashboard(request):
    user = User.objects.get(pk=request.user.id)

    current_date = datetime.date.today() 

    if user.role == 1:
        tutor = Tutor.objects.get(user=user)
        scheduled_lessons = Schedule.objects.filter(tutor=tutor, date__gte=current_date, student__isnull=False).order_by('date', 'time')
    elif user.role == 2:
        student = Student.objects.get(user=user)
        scheduled_lessons = Schedule.objects.filter(student=student, date__gte=current_date).order_by('date', 'time')
    else:
        scheduled_lessons = Schedule.objects.filter(student__isnull=False, date__gte=current_date).order_by('date', 'time')


    return render(request, "tutormanager/dashboard.html", {
        "upcoming_lessons": scheduled_lessons
    })


@login_required
def profile(request, id):
    profile_user = User.objects.get(pk=id)

    if profile_user.role == 1: # Tutor
        tutor = Tutor.objects.get(user=profile_user)

        # Retrieve student feedback
        if Feedback.objects.filter(tutor=tutor).exists():
            feedback = Feedback.objects.filter(tutor=tutor).order_by('-datetime')
        else: 
            feedback = None

        return render(request, "tutormanager/tutor_profile.html", {
            "tutor": tutor.serialize(),
            "star_count": tutor.star.count(),
            "star_list": tutor.star,
            "student_feedback": feedback,
        })

    elif profile_user.role == 2: # Student
        student = Student.objects.get(user=profile_user)
        
        return render(request, "tutormanager/student_profile.html", {
            "student": student.serialize(),
        })

    else:
        return render(
            request, "tutormanager/profile.html", {
            "profile_user": profile_user,
        })


@login_required
def edit_profile(request, id):
    if not request.user.id == id:
        return JsonResponse({"error": "Unable to edit profile."}, status=404)

    profile_user = User.objects.get(pk=id)

    if request.method == "POST":    
        data = json.loads(request.body)
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        print(first_name)

        if Tutor.objects.filter(user=profile_user).exists():    
            experience_years = data.get("experience_years")
            bio = data.get("bio")
            
            tutor = Tutor.objects.get(user=profile_user)
            profile_user.first_name = first_name
            profile_user.last_name = last_name
            tutor.experience_years = experience_years
            tutor.bio = bio

            profile_user.save()
            tutor.save()

            return JsonResponse({"message": "Profile updated successfully."}, status=201)

        elif Student.objects.filter(user=profile_user).exists():
            acad_level = data.get("acad_level")
            school = data.get("school")

            student = Student.objects.get(user=profile_user)
            profile_user.first_name = first_name
            profile_user.last_name = last_name
            student.acad_level = acad_level
            student.school = school

            profile_user.save()
            student.save()

            return JsonResponse({"message": "Profile updated successfully."}, status=201)

        JsonResponse({"error": "Unable to update profile."}, status=404)
                    
    elif request.method == "GET":
        if Tutor.objects.filter(user=profile_user).exists():
            profile_user = Tutor.objects.get(user=profile_user)

        elif Student.objects.filter(user=profile_user).exists():
            profile_user = Student.objects.get(user=profile_user)

        return JsonResponse(profile_user.serialize())


@login_required
def star_profile(request, id):
    if request.method == "POST":
        tutor_user = User.objects.get(pk=id)
        tutor = Tutor.objects.get(user=tutor_user)

        # User who star-ed profile
        user = User.objects.get(pk=request.user.id)

        star_count = tutor.star.count()

        tutor.star.add(user)
        tutor.save()

        return JsonResponse({"message": "Profile star-ed successfully.",
                            "star_count": star_count + 1}, status=201)
    else:
       return JsonResponse({"error": "Error star-ing profile."}, status=404)

@login_required
def unstar_profile(request,id):
    if request.method == "POST":
        tutor_user = User.objects.get(pk=id)
        tutor = Tutor.objects.get(user=tutor_user)

        # User who unstar-ed profile
        user = User.objects.get(pk=request.user.id)

        star_count = tutor.star.count()

        tutor.star.remove(user)
        tutor.save()

        return JsonResponse({"message": "Profile unstar-ed successfully.",
                            "star_count": star_count - 1}, status=201)
    
    else:
        return JsonResponse({"error": "Error unstar-ing profile."}, status=404)


@login_required
def feedback(request, id):
    if request.method == "POST":
        # Access info from form data
        comment = request.POST["comment"]
        
        student = Student.objects.get(user=request.user)

        user_tutor = User.objects.get(pk=id)
        tutor = Tutor.objects.get(user=user_tutor)

        # Create Feedback object
        fb = Feedback (
            student = student,
            tutor = tutor,
            comment = comment,
        )

        # Insert new Feedback into database
        fb.save()

        return HttpResponseRedirect(reverse('profile', args={id}))
    

@login_required
def search_tutors(request):
    is_filtered = False
    username = ""

    if request.method == "POST" and (len(request.POST.get("search-username")) > 0):
        username = request.POST.get("search-username")
        users = User.objects.filter(username__contains=username)
        tutors = Tutor.objects.filter(user__in=users)
        is_filtered = True
    else:
        tutors = Tutor.objects.all()

    if tutors != None:
        paginator = Paginator(tutors, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, "tutormanager/search_tutors.html", {
        "tutors": page_obj,
        "is_filtered": is_filtered,
        "username": username
    })


@login_required
def lesson_record(request):
    user = User.objects.get(pk=request.user.id)

    if user.role == 1:
        tutor = Tutor.objects.get(user=user)
        records = Lesson.objects.filter(tutor=tutor).order_by('-date', '-time')
    elif user.role == 2:
        student = Student.objects.get(user=user)
        records = Lesson.objects.filter(student=student).order_by('-date', '-time')
    else:
        records = Lesson.objects.all().order_by('-date', '-time')

    return render(request, "tutormanager/lesson_record.html", {
        "records": records
    })


@login_required
@user_passes_test(lambda u: u.groups.filter(name='TUTOR').exists())
def add_lesson(request):
    if request.method == "POST":

        tutor_id = request.user.id
        student_username = request.POST.get("student")
        lesson_date = request.POST.get("lesson-date")
        lesson_time = request.POST.get("lesson-time")
        comment = request.POST.get("comment")

        if User.objects.filter(username=student_username).exists():
            user_student = User.objects.get(username=student_username)

            if Student.objects.filter(user=user_student).exists():
                student = Student.objects.get(user=user_student)

                user_tutor = User.objects.get(pk=tutor_id)
                tutor = Tutor.objects.get(user=user_tutor)
  
                # Create Lesson
                lesson = Lesson(
                    student = student,
                    tutor = tutor,
                    date = lesson_date,
                    time = lesson_time,
                    comment = comment,
                )

                lesson.save()

                return render(request, 'tutormanager/add_lesson.html', {
                    "has_alert": True,
                    "is_successful": True
                })
        
        return render (request, 'tutormanager/add_lesson.html', {
                    "has_alert": True,
                    "is_successful": False
                })

    else:
        return render(request, 'tutormanager/add_lesson.html', {
            "has_alert": False,
        })
    

@login_required
@user_passes_test(lambda u: u.groups.filter(name='TUTOR').exists())
def delete_lesson(request, id):
    Lesson.objects.filter(pk=id).delete()
    return lesson_record(request)
    

@login_required
@user_passes_test(lambda u: u.groups.filter(name='TUTOR').exists())
def add_availability(request):
    if request.method == "GET":

        current_date = datetime.date.today()
        
        tutor = Tutor.objects.get(user=request.user)
        available_slots = AvailableSlot.objects.filter(tutor=tutor, date__gte=current_date).order_by('date', 'time')

        return render (request, 'tutormanager/tutor_availability.html', {
            "available_slots": available_slots
        })
    
    if request.method == "POST":
        slot_date = request.POST.get("available-date")
        slot_time = request.POST.get("available-time")

        tutor = Tutor.objects.get(user=request.user)

        new_slot = AvailableSlot(
            tutor=tutor,
            date=slot_date,
            time=slot_time
        )

        new_slot.save()

        return HttpResponseRedirect(reverse('add_availability'))
    

@login_required
@user_passes_test(lambda u: u.groups.filter(name='TUTOR').exists())
def delete_availability(request, id):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=404)

    slot = AvailableSlot.objects.get(pk=id)
    
    if slot.tutor.user == request.user:
        slot.delete()
        return JsonResponse({"message": "Available slot deleted successfully"}, status=201)

    return JsonResponse({"error": "Unable to delete available slot."}, status=404)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='STUDENT').exists())
def view_tutor_availability(request):

    tutors = Tutor.objects.all()

    if request.method == "GET":
        return render(request, 'tutormanager/student_add_schedule.html', {
            "tutors": tutors
        })

    if request.method == "POST":
        tutor_id = request.POST.get('tutor-id')
        
        tutor = Tutor.objects.get(pk=tutor_id)
        current_date = datetime.date.today()
        available_slots = AvailableSlot.objects.filter(tutor=tutor, date__gte=current_date, taken=False).order_by('date', 'time')

        return render(request, 'tutormanager/student_add_schedule.html', {
            "available_slots": available_slots,
            "tutors": tutors
        })


@login_required
@user_passes_test(lambda u: u.groups.filter(name='STUDENT').exists())
def add_schedule(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=404)
    
    slot = AvailableSlot.objects.get(pk=id)
    student = Student.objects.get(user=request.user)
    
    new_schedule = Schedule(
        student=student,
        tutor=slot.tutor,
        date=slot.date,
        time=slot.time
    )

    new_schedule.save()

    slot.taken = True
    slot.save()

    return JsonResponse({"message": "Lesson slot scheduled successfully",
                         "date": slot.date,
                         "time": slot.time,
                         }, status=201)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='STUDENT').exists())
def cancel_schedule(request, id):
    if request.method == "POST":
        
        schedule = Schedule.objects.get(pk=id)

        if schedule.student.user != request.user:
            return JsonResponse({"error": "You can only cancel your own scheduled lesson"}, status=404)

        slot = AvailableSlot.objects.get(tutor=schedule.tutor, date=schedule.date, time=schedule.time, taken=True)
        slot.taken = False
        slot.save()
        schedule.delete()

        return JsonResponse({"message": "Scheduled lesson cancelled successfully."}, status=201)
    
    return JsonResponse({"error": "POST request required."}, status=404)
