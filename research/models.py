from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class ResearchSession(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='research_sessions'
    )

    query = models.TextField()

    final_report = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING'
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    trace_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    craeted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"ResearchSession {self.id} - {self.status}"
    


class ResearchSummary(models.Model):
    research = models.OneToOneField(
        ResearchSession,
        on_delete=models.CASCADE,
        related_name='summary'
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)



class ResearchReasoning(models.Model):
    research = models.OneToOneField(
        ResearchSession,
        on_delete=models.CASCADE,
        related_name='reasoning'
    )

    content = models.TextField(
        help_text="High-level reasoning summary (no chain-of-thought)"
    )

    creted_at = models.DateTimeField(auto_now_add=True)


class ResearchCost(models.Model):
    research = models.OneToOneField(
        ResearchSession,
        on_delete=models.CASCADE,
        related_name='cost'
    )

    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)

    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=4,
    )

    created_at = models.DateTimeField(auto_now_add=True)


class UploadedDocument(models.Model):
    research = models.ForeignKey(
        ResearchSession,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    file = models.FileField(upload_to='research_docs/')
    extracted_text = models.TextField()
    summary = models.TextField()

    uploaded_at = models.DateTimeField(auto_now_add=True)


