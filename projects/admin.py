from django.contrib import admin
from django.utils.html import mark_safe, format_html
from projects.models import Project, ProjectFiles, ProjectUser


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'stuff_list')
    sortable_by = ()
    exclude = ('is_deleted',)

    def stuff_list(self, obj):
        pusers = ProjectUser.objects.filter(project_id=obj.id, is_deleted=0)
        users = [i.user.name for i in pusers if i.user.name]
        datas = "<br/>".join(users)
        return format_html(datas)

    stuff_list.short_description = "成员"

    def get_queryset(self, request):
        qs = super(ProjectAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        if not request.user.is_superuser:
            qs = qs.filter(projectuser__user_id=request.user.id)
        return qs

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Project, ProjectAdmin)
