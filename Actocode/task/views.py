from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import render
from task.models import Task
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Submission, Task , UserProfile
from .serializers import SubmissionSerializer,UserProfileSerializer
import subprocess
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from task.models import UserProfile
from task.models import Transaction
from .models import Profile
from task.models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import login
from task.forms import UserRegistrationForm
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Submission, Task
from .serializers import SubmissionSerializer
from django.contrib.auth.models import User

class TaskViewSet(viewsets.ModelViewSet):
    """API for listing and managing tasks"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']  # Allow Read/Write for admin


def task_list(req):
    """View to display available tasks"""
    tasks = Task.objects.all()
    return render(req,"task.html",{"tasks": tasks})



class SubmissionViewSet(viewsets.ModelViewSet):
    """API for submitting and evaluating code"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Handle code submission and evaluate it"""
        user = request.user
        task_id = request.data.get("task")
        code = request.data.get("code")

        if not task_id or not code:
            return Response({"error": "Task and code are required"}, status=400)

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)

        # Save the submission
        submission = Submission.objects.create(user=user, task=task, code=code)

        # Compare user-submitted code with correct code
        is_correct = submission.code.strip() == task.correct_code.strip()
        submission.is_correct = is_correct
        submission.status = "approved" if is_correct else "rejected"
        submission.save()

        if is_correct:
    # Debugging: Check if user has a profile
            user_profile, created = UserProfile.objects.get_or_create(user=user)
        
            user_profile.coins += task.reward_coins
            user_profile.save()
            print(f"After Update: {user.username} has {user_profile.coins} coins.")

        return Response({
            "message": "Submission received",
            "status": submission.status
        })
    def evaluate_code(self, task, code):
        """Evaluate user-submitted code (Basic Python execution)"""
        try:
            # Run the code in a safe subprocess
            result = subprocess.run(
                ["python3", "-c", code], capture_output=True, text=True, timeout=3
            )
            output = result.stdout.strip()
            
            # Simple evaluation (You can replace this with real test cases)
            expected_output = "Hello, World!"  # Example expected output
            return output == expected_output

        except Exception as e:
            return False


@login_required
def submission_list(request):
    submissions = Submission.objects.filter(user=request.user)
    return render(request, "submission_list.html", {"submissions": submissions})

class UserProfileViewSet(viewsets.ModelViewSet):
    """API to get user coin balance"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "dashboard.html", {"user_profile": user_profile, "transactions": transactions })


# User Signup
def register_user(request):
    if request.method == "POST":   
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists(): # type: ignore
            messages.error(request, "Username already taken!")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password) # type: ignore
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "register.html")

# User Login

@csrf_protect
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("prant")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")
def profile(req):
    return render(req,'profile.html')
def base(req):
    return render(req,'base.html')
def code_editor2(request):
    
    tasks = Task.objects.all()
    
    if request.method == "POST":
        task_id = request.POST.get("task")
        code = request.POST.get("code")

        if task_id and code:
            task = Task.objects.get(id=task_id)
            submission = Submission.objects.create(user=request.user, task=task, code=code)

            # Compare submitted code with correct code
            submission.is_correct = submission.code.strip() == task.correct_code.strip()
            submission.status = "approved" if submission.is_correct else "rejected"
            submission.save()

            return render(request, "editor2.html", {"tasks": tasks, "result": submission.status})

    return render(request, "editor2.html", {"tasks": tasks})
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "profile.html", {"profile": profile})
   
# User Logout
def logout_user(request):
    logout(request)
    return redirect("home")

# API for JWT Login
@api_view(["POST"])
def api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})

    return Response({"error": "Invalid credentials"}, status=400)


@login_required
def withdraw_coins(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        amount = int(request.POST.get("amount"))

        if amount > user_profile.coins:
            messages.error(request, "Insufficient coins!")
        else:
            user_profile.coins -= amount
            user_profile.save()
            messages.success(request, f"Successfully withdrawn {amount} coins!")

    return render(request, "withdraw.html", {"coins": user_profile.coins})

@login_required
def redeem_voucher(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        voucher_cost = 100  # Example: 100 coins per voucher

        if user_profile.coins < voucher_cost:
            messages.error(request, "Not enough coins to redeem a voucher!")
        else:
            user_profile.coins -= voucher_cost
            user_profile.save()
            messages.success(request, "Voucher redeemed successfully!")

    return render(request, "redeem.html", {"coins": user_profile.coins})
@login_required
def withdraw_coins(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        amount = int(request.POST.get("amount"))

        if amount > user_profile.coins:
            messages.error(request, "Insufficient coins!")
        else:
            user_profile.coins -= amount
            user_profile.save()

            # Save transaction
            Transaction.objects.create(user=request.user, transaction_type="withdraw", amount=amount)

            messages.success(request, f"Successfully withdrawn {amount} coins!")

    return render(request, "withdraw.html", {"coins": user_profile.coins})

@login_required
def redeem_voucher(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        voucher_cost = 100  # Example: 100 coins per voucher

        if user_profile.coins < voucher_cost:
            messages.error(request, "Not enough coins to redeem a voucher!")
        else:
            user_profile.coins -= voucher_cost
            user_profile.save()

            # Save transaction
            Transaction.objects.create(user=request.user, transaction_type="redeem", amount=voucher_cost)

            messages.success(request, "Voucher redeemed successfully!")

    return render(request, "redeem.html", {"coins": user_profile.coins})

def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by("-timestamp")

    return render(request, "dashboard.html", {"coins": user_profile.coins, "transactions": transactions})

# Create your views here.


def main_views(req, *args, **kwargs):
    code = str(kwargs.get("ref_code"))
    try:
        Profile = Profile.objects.get(code=code)
        req.session['ref_profile'] = Profile.id
        print('id',Profile.id)
    except:
        pass
    print(req.session.get_expiry_date())
    return render(req,"register.html",{})



def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)  # Task fetch karna database se
    return render(request, 'editor2.html', {'task': task})


from django.http import JsonResponse
import json
from .models import Task  # Ensure Task model is imported

def compile_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            lang = data.get("lang", "")
            task_id = data.get("task_id")

            if not code or not lang or not task_id:
                return JsonResponse({"error": "Code, language, and task ID are required"}, status=400)

            # Task ka correct answer database se fetch karein
            try:
                task = Task.objects.get(id=task_id)
                correct_output = task.correct_output.strip()
            except Task.DoesNotExist:
                return JsonResponse({"error": "Invalid Task ID"}, status=400)

            # ⚡ Execute the user's code (Replace with actual execution logic)
            user_output = "5"  # ❗ Replace with actual executed code output
            
            print(f"User Output: '{user_output}'")  # Debugging
            print(f"Correct Output: '{correct_output}'")  # Debugging

            # ✅ Compare user output with correct output (Remove extra spaces & newlines)
            is_correct = user_output.strip() == correct_output.strip()

            return JsonResponse({
                "output": user_output,
                "is_correct": is_correct
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
from django.shortcuts import render
from .models import Task  # Import your Task model

def submit_solution(request):
    tasks = Task.objects.all()  # Fetch all tasks from the database
    return render(request, 'editor2.html', {'tasks': tasks})
