from django.contrib import admin

from knowledges.models import Knowledge
from knowledges.views import knowledge_list_page
from common.utils import logger


class KnowledgeAdmin(admin.ModelAdmin):
    exclude = ('is_deleted',)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        user = request.user
        if not user.is_superuser:
            self.change_form_template = "knowledge/change_form.html"
            extra_context = extra_context or {}
            knowledge = Knowledge.objects.filter(id=object_id).first()
            extra_context['knowledge'] = knowledge
            extra_context['user'] = user
        return super(KnowledgeAdmin, self).change_view(request, object_id, form_url=form_url,
                                                    extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        return knowledge_list_page(request)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Knowledge, KnowledgeAdmin)
