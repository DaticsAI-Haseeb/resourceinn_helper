from django.db import models


# Create your models here.

class AuditTrailModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AuditTrailModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ActionChoices(models.TextChoices):
    CHECK_IN = "check_in"
    CHECK_OUT = "check_out"
    BREAK_IN = "break_in"
    BREAK_OUT = "break_out"


class ActionStatus(models.TextChoices):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    SCHEDULING = "scheduling"
    SCHEDULED = "scheduled"


class Log(AuditTrailModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ActionChoices.choices)
    status = models.CharField(max_length=50, choices=ActionStatus.choices, default=ActionStatus.IN_PROGRESS)

    def __str__(self):
        return f"{self.user.name}"