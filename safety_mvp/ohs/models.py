# Updated MVP Django App Structure for OHS ISO 45001 Tool

from django.db import models
from django.contrib.auth.models import User

# Incident Reporting
class Incident(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_reported = models.DateField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='incidents/', blank=True, null=True)
    incident_file = models.FileField(upload_to='incidents/files/', blank=True, null=True)  # <-- Add this
    location = models.CharField(max_length=255)
    severity = models.CharField(max_length=50, choices=[
        ('Near Miss', 'Near Miss'),
        ('First Aid', 'First Aid'),
        ('Medical Treatment', 'Medical Treatment'),
        ('Lost Time', 'Lost Time'),
        ('Fatality', 'Fatality'),
    ])

# JSA (Job Safety Analysis)
class JSA(models.Model):
    task = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    hazards = models.TextField()
    controls = models.TextField()
    signed = models.BooleanField(default=False)
    jsa_file = models.FileField(upload_to='jsa/files/', blank=True, null=True)  # <-- Add this

# FRA (Formal Risk Assessment)
class FRA(models.Model):
    activity = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    risk_identified = models.TextField()
    risk_level = models.CharField(max_length=50)
    control_measures = models.TextField()
    assessed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_assessed = models.DateField(auto_now_add=True)
    fra_file = models.FileField(upload_to='fra/files/', blank=True, null=True)  # <-- Add this

# FLRA (Field Level Risk Assessment)
class FLRA(models.Model):
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=255)
    assessed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    task_description = models.TextField()
    identified_hazards = models.TextField()
    control_measures = models.TextField()
    flra_file = models.FileField(upload_to='flra/files/', blank=True, null=True)  # <-- Add this

# SDS and SOP
class Document(models.Model):
    DOC_TYPE_CHOICES = [
        ('SDS', 'Safety Data Sheet'),
        ('SOP', 'Standard Operating Procedure')
    ]
    name = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=10, choices=DOC_TYPE_CHOICES)
    related_material = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True, blank=True)
    upload_date = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')

# Material and related SDS
class Material(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_received = models.DateField()
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    sds_available = models.BooleanField(default=False)
    material_file = models.FileField(upload_to='materials/files/', blank=True, null=True)  # <-- Add this

# PTO/CCV - Planned Task Observation / Critical Control Verification
class Observation(models.Model):
    observed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    task = models.CharField(max_length=255)
    observation_type = models.CharField(max_length=10, choices=[
        ('PTO', 'Planned Task Observation'),
        ('CCV', 'Critical Control Verification')
    ])
    controls_verified = models.TextField()
    findings = models.TextField()
    follow_up_required = models.BooleanField(default=False)
    attachments = models.ManyToManyField('Document', blank=True)
    file = models.FileField(upload_to='observations/', blank=True, null=True)  # Already present

# Safety Checklists (Daily, Weekly, Monthly - ISO 45001 aligned)
class SafetyChecklist(models.Model):
    TYPE_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly')
    ]
    checklist_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    completed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_completed = models.DateField(auto_now_add=True)
    ppe_inspection = models.BooleanField(default=False)
    fire_safety_check = models.BooleanField(default=False)
    equipment_condition = models.BooleanField(default=False)
    emergency_exits_clear = models.BooleanField(default=False)
    safety_signage_visible = models.BooleanField(default=False)
    first_aid_kit_stocked = models.BooleanField(default=False)
    housekeeping_checked = models.BooleanField(default=False)
    comments = models.TextField(blank=True, null=True)
    checklist_file = models.FileField(upload_to='checklists/files/', blank=True, null=True)  # <-- Add this

# Certification Tracking
class Certification(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    issuing_body = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    certificate_file = models.FileField(upload_to='certifications/', blank=True, null=True)  # Already present

# Contractor Onboarding
class Contractor(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    id_document = models.FileField(upload_to='contractors/ids/', blank=True, null=True)  # Already present
    certifications = models.ManyToManyField(Certification, blank=True)
    onboarded = models.BooleanField(default=False)
    onboarding_date = models.DateField(auto_now_add=True)
    contractor_file = models.FileField(upload_to='contractors/files/', blank=True, null=True)  # <-- Add this

# Employee Model (to track internal employees separately from User auth)
class Employee(models.Model):
    name = models.CharField(max_length=255, default="Unknown")
    position = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=255)
    certifications = models.ManyToManyField(Certification, blank=True, related_name="employees")
    employee_file = models.FileField(upload_to='employees/files/', blank=True, null=True)  # <-- Add this

# Objectives Model
class Objective(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    target = models.TextField()
    current = models.PositiveIntegerField(default=0)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('not started', 'Not Started'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='not started')
    due_date = models.DateField(null=True, blank=True)
    objective_file = models.FileField(upload_to='objectives/files/', blank=True, null=True)  # <-- Add this

    def progress_percent(self):
        if self.target > 0:
            return min(100, int((self.current / self.target) * 100))
        return 0

    def __str__(self):
        return self.name

# Training Matrix
class TrainingMatrix(models.Model):
    TRAINING_STATUS_CHOICES = [
        ('not started', 'Not Started'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_employees = models.ManyToManyField(Employee, related_name="trainings")
    training_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TRAINING_STATUS_CHOICES, default='not started')
    training_material = models.FileField(upload_to='training/files/', blank=True, null=True)
    certificate_required = models.BooleanField(default=False)
    certificate_upload = models.FileField(upload_to='training/certificates/', blank=True, null=True)

    def __str__(self):
        return self.title
