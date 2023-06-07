from django.contrib import admin
from .models import Patient, Appointment


class AppointmentAdmin(admin.ModelAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = Appointment
    list_display = ("date", "status", "doctor","patient",)
    list_filter = ("date", "status", "doctor","patient",)
    fieldsets = (
        (None, {"fields": ("date", "time", "patient", "doctor","status")}),
        ("Szczegóły", {"fields": ( "reason", "prescription", "recommendations", "room")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "date", "time", "patient", "doctor", "reason","status"
            )}
        ),
    )
    search_fields = ("date",)
    ordering = ("date",)


admin.site.register(Patient)
admin.site.register(Appointment, AppointmentAdmin)

