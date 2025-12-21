from django.conf import settings
from django.db import models
from django.db.models import Sum


class UserProfile(models.Model):
    """
    Extends Django's built-in User with a simple role system.
    """
    ROLE_ADMIN = "ADMIN"
    ROLE_DONOR = "DONOR"
    ROLE_RECIPIENT = "RECIPIENT"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_DONOR, "Donor"),
        (ROLE_RECIPIENT, "Recipient"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class DonationProject(models.Model):
    STATUS_ACTIVE = "ACTIVE"
    STATUS_COMPLETED = "COMPLETED"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_COMPLETED, "Completed"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    illness_type = models.CharField(max_length=100)
    total_estimated_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def total_collected_amount(self):
        result = self.donations.aggregate(total=Sum("amount"))
        return result["total"] or 0


class RecipientRequest(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipient_requests",
    )
    full_name = models.CharField(max_length=200)
    age = models.IntegerField()
    medical_condition = models.TextField()
    hospital_name = models.CharField(max_length=200)
    treatment_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    financial_condition = models.TextField()
    medical_document = models.FileField(
        upload_to="medical_docs/",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.recipient.username}"

    ai_recommended_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AI-recommended allocation amount"
    )

    ai_explanation = models.TextField(
        null=True,
        blank=True,
        help_text="Explanation of AI allocation decision"
    )


class Donation(models.Model):
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="donations",
    )
    project = models.ForeignKey(
        DonationProject,
        on_delete=models.CASCADE,
        related_name="donations",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Donation {self.amount} by {self.donor.username} to {self.project.name}"
