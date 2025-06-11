from django.shortcuts import render
from .models import Incident, JSA, FRA, FLRA, Document, Material, Observation, SafetyChecklist, Certification, Contractor, Employee, Objective

TARGETS = {
    'observation': 20,   # CCV including PTO
    'flra': 500,
    'jsa': 15,
    'fra': 1,
    # SDS and SOP have no count/target
    # The rest don't need a target
}

def home(request):
    data = {
        'incident_count': Incident.objects.count(),
        'jsa_count': JSA.objects.count(),
        'fra_count': FRA.objects.count(),
        'flra_count': FLRA.objects.count(),
        'document_count': Document.objects.count(),
        'material_count': Material.objects.count(),
        'observation_count': Observation.objects.count(),
        'safetychecklist_count': SafetyChecklist.objects.count(),
        'certification_count': Certification.objects.count(),
        'contractor_count': Contractor.objects.count(),
        'employee_count': Employee.objects.count(),

        # Targets for bar chart
        'observation_target': TARGETS['observation'],
        'flra_target': TARGETS['flra'],
        'jsa_target': TARGETS['jsa'],
        'fra_target': TARGETS['fra'],
    }
    objectives = Objective.objects.all()
    return render(request, 'home.html', {
        **data,
        'objectives': objectives,
    })
