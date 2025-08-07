from django import forms
from django.contrib.auth.models import User
from task.models import Profile

class UserRegistrationForm(forms.ModelForm):
    referral_code = forms.CharField(max_length=12, required=False, label="Referral Code (Optional)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            referral_code = self.cleaned_data.get("referral_code")
            if referral_code:
                try:
                    referrer_profile = Profile.objects.get(code=referral_code)
                    user.profile.recommended_by = referrer_profile.user
                    user.profile.save()
                except Profile.DoesNotExist:
                    pass  # Invalid referral code, just ignore
        return user 
