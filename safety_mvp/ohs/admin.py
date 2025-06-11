from django.contrib import admin
from .models import (
    Incident,
    JSA,
    FRA,
    FLRA,
    Document,
    Material,
    Observation,
    SafetyChecklist,
    Certification,
    Contractor,
    Employee,
    Objective,
    TrainingMatrix,  # ✅ Add this
)

@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'target', 'current', 'status', 'assigned_to', 'due_date')
    list_filter = ('status', 'assigned_to')
    search_fields = ('name', 'description')


@admin.register(TrainingMatrix)
class TrainingMatrixAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'training_date', 'due_date', 'certificate_required')
    list_filter = ('status', 'certificate_required')
    search_fields = ('title', 'description')

admin.site.register(Incident)
admin.site.register(JSA)
admin.site.register(FRA)
admin.site.register(FLRA)
admin.site.register(Document)
admin.site.register(Material)
admin.site.register(Observation)
admin.site.register(SafetyChecklist)
admin.site.register(Certification)
admin.site.register(Contractor)
admin.site.register(Employee)

# Change admin site header
admin.site.site_header = "ISO CSystem"
admin.site.site_title = "ISO CSystem Admin"
admin.site.index_title = "Welcome to ISO_CSystem Administration"
