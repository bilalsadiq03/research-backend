from django.contrib import admin
from .models import (
    ResearchSession, 
    ResearchSummary,
    ResearchReasoning,
    ResearchCost,
    UploadedDocument
)

# Register your models here.

admin.site.register(ResearchSession)
admin.site.register(ResearchSummary)
admin.site.register(ResearchReasoning)
admin.site.register(ResearchCost)
admin.site.register(UploadedDocument)
