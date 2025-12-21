from django.contrib import admin
from django.contrib import messages
from .models import UserProfile, DonationProject, RecipientRequest, Donation
from core.ai.allocation_engine import run_ai_allocation


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "created_at", "updated_at")
    list_filter = ("role", "created_at")
    search_fields = ("user__username", "user__email", "role")

@admin.action(description="Run AI Allocation for selected project(s)")
def run_ai_allocation_action(modeladmin, request, queryset):
    for project in queryset:
        result = run_ai_allocation(project)
        messages.success(request, f"{project.name}: {result}")

class DonationProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "illness_type",
        "total_estimated_amount",
        "total_collected_amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "illness_type", "created_at")
    search_fields = ("name", "description", "illness_type")
    actions = [run_ai_allocation_action]


class RecipientRequestAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "full_name",
        "status",
        "treatment_cost",
        "ai_recommended_amount",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "recipient__username",
        "recipient__email",
        "full_name",
        "hospital_name",
        "medical_condition",
    )
    readonly_fields = ("created_at", "ai_recommended_amount", "ai_explanation")
    
    def approve_request(self, request, queryset):
        queryset.update(status=RecipientRequest.STATUS_APPROVED)
    approve_request.short_description = "Approve selected requests"
    
    def reject_request(self, request, queryset):
        queryset.update(status=RecipientRequest.STATUS_REJECTED)
    reject_request.short_description = "Reject selected requests"
    
    actions = [approve_request, reject_request]


class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "donor",
        "project",
        "amount",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "donor__username",
        "donor__email",
        "project__name",
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DonationProject, DonationProjectAdmin)
admin.site.register(RecipientRequest, RecipientRequestAdmin)
admin.site.register(Donation, DonationAdmin)
