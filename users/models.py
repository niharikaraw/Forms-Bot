from unicodedata import name
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True)
    organization = models.CharField(max_length=255, null=True)
    is_premium = models.BooleanField(default=False)
    is_waitlisted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.first_name)


class Campaign(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
   # logo = models.FileField(null=True, blank=True,upload_to='Logo')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_message = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.title)


class Bots(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    intro_text = models.CharField(max_length=255, null=True)
    end_message = models.CharField(max_length=255, null=True)
    avatar_image = models.FileField(null=True, blank=True, upload_to='Avatar Image')
    intro_image = models.FileField(null=True, blank=True, upload_to='Intro Image')
    background_url = models.CharField(max_length=255, null=True)
    help_text = models.CharField(max_length=255, null=True)
    uid = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.title)


class BotsCampaignMapping(models.Model):
    bot_id = models.ForeignKey(Bots, on_delete=models.CASCADE, null=True)
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)


class Questions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    bot_id = models.ForeignKey(Bots, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=255, null=True)
    question_sequence = models.IntegerField(null=True)
    helper_text = models.CharField(max_length=255, null=True)
    is_multiple = models.BooleanField(default=False, null=True)
    is_checkbox = models.BooleanField(default=False, null=True)


class Options(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)
    option_text = models.CharField(max_length=255, null=True)
    option_sequence = models.IntegerField(null=True)


class Responses(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)
    option_id = models.ForeignKey(Options, on_delete=models.CASCADE, null=True)
    bot_id = models.ForeignKey(Bots, on_delete=models.CASCADE, null=True)
    uid = models.CharField(max_length=255, unique=True, blank=True, null=True)


class Subscriptions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=-True)
    type = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False, null=True)
    payment_id = models.CharField(max_length=20, null=True)
    order_id = models.CharField(max_length=25, null=True)
    timestamp = models.DateTimeField(auto_created=True)
    amount = models.IntegerField(null=True)

    def __str__(self):
        return str(self.order_id)


class ContactUs(models.Model):
    email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    text = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(default=timezone.now)


class Feedback(models.Model):
    bot = models.ForeignKey(Bots, on_delete=models.CASCADE,null=True)
    rating = models.FloatField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
