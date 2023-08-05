from django.contrib import admin
from .models import Workflow


class WorkflowAdmin(admin.ModelAdmin):
    @staticmethod
    def _forms_data(obj):
        return obj.get_decoded()

    list_display = [
        'session_key',
        'email',
        'url_full_results',
        '_forms_data',
        'expire_date'
    ]


admin.site.register(Workflow, WorkflowAdmin)
