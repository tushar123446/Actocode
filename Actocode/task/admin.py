from django.contrib import admin
from .models import Task,Profile
from task.models import Submission
from django.contrib import admin
from task.models import Submission,UserProfile
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "reward_coins", "created_at" ,"correct_code",)
    search_fields = ("title",)
    list_filter = ("difficulty",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "status", "submitted_at")
    search_fields = ("user__username", "task__title")
    list_filter = ("status", "submitted_at")


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'status','is_correct','submitted_at')
    list_filter = ('status','is_correct',)
    search_fields = ('user__username', 'task__title')
    actions = ['approve_submission', 'reject_submission']

    def approve_submission(self, request, queryset):
        queryset.update(status="approved")
    approve_submission.short_description = "Approve selected submissions"

    def reject_submission(self, request, queryset):
        queryset.update(status="rejected")
    reject_submission.short_description = "Reject selected submissions"

admin.site.register(Profile)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins')  # Show these fields in the admin list view
    search_fields = ('user__username',)  # Allow searching by username
    list_filter = ('coins',)  # Add filter by coins
