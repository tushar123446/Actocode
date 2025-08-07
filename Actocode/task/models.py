 
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from .utils import generete_ref_code
from django.db import models
from django.contrib.auth.models import User
 
class Task(models.Model):
    DIFFICULTY_LEVELS = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default="Easy")
    reward_coins = models.IntegerField(default=10)  # Coins awarded for completion
    created_at = models.DateTimeField(auto_now_add=True)
    correct_code = models.TextField(default="print('Hello, World!')", blank=True )

    def __str__(self):
        return self.title





class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    code = models.TextField()  # This is the submitted code
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)  # Stores whether the submission is correct

    
    def is_correct(self):
        """Compare user-submitted code with the correct code"""
        return self.code.strip() == self.task.correct_code.strip()

    def check_submission(self):
        """Check if the submitted code matches the correct code"""
        return self.code.strip() == self.task.correct_code.strip()

    def save(self, *args, **kwargs):
        """Before saving, check if the submission is correct"""
        self.is_correct = self.check_submission()
        super().save(*args, **kwargs) 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)  # Coin balance

    def __str__(self):
        return f"{self.user.username} - {self.coins} coins"

# Automatically create a UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)  # Store user coins

    def __str__(self):
        return self.user.username

 
 

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("withdraw", "Withdraw"),
        ("redeem", "Redeem"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12 , blank=True)
    recommended_by = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null= True, related_name="Ref_by")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.username}-{self.code}"
    def get_recommened_profile( self):
        pass
    def save(self, *args, **kwargs):
        if self.code == "":
            code = generete_ref_code()  
            self.code = code
        super().save(*args, **kwargs)
def generate_referral_code():
    """Generate a unique 6-character referral code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

