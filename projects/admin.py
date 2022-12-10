from django.contrib import admin
from django.utils.html import mark_safe, format_html
from projects.models import Project, ProjectFiles, ProjectUser, PythonTrain


class ProjectFilesInline(admin.TabularInline):
    model = ProjectFiles
    extra = 1
    exclude = ('is_deleted',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'stuff_list')
    sortable_by = ()
    exclude = ('is_deleted',)
    show_full_result_count = False

    def stuff_list(self, obj):
        pusers = ProjectUser.objects.filter(project_id=obj.id, is_deleted=0)
        users = [i.user.name for i in pusers if i.user.name]
        datas = "<br/>".join(users)
        return format_html(datas)

    stuff_list.short_description = "成员"

    def get_queryset(self, request):
        qs = super(ProjectAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        # if not request.user.is_superuser:
        #     qs = qs.filter(projectuser__user_id=request.user.id)
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


class ProjectFilesAdmin(admin.ModelAdmin):
    list_display = ('project', 'file_url', 'sort', 'created')
    exclude = ('is_deleted',)
    show_full_result_count = False
    sortable_by = ()

    def file_url(self, obj):
        if not obj.file:
            return ''
        return format_html(obj.file.url)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class PythonTrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'code_txt', 'created')
    list_display_links = ('code_txt',)
    list_filter = ('user',)
    exclude = ('is_deleted',)
    show_full_result_count = False
    # actions_selection_counter = False
    sortable_by = ()

    def code_txt(self, obj):
        return mark_safe(obj.code[:20])

    code_txt.short_description = "代码"

    def user_name(self, obj):
        return format_html(obj.user.name)

    user_name.short_description = "学生"

    def get_queryset(self, request):
        qs = super(PythonTrainAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        if not request.user.is_superuser:
            qs = qs.filter(user_id=request.user.id)
        return qs

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.list_display = ('id', 'code_txt', 'created')
            self.list_filter = ()
        return super(PythonTrainAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        user = request.user
        self.change_form_template = "python_train/change_form.html"
        extra_context = extra_context or {}
        train = PythonTrain.objects.filter(id=object_id).first()
        extra_context['user'] = user
        extra_context['sid'] = object_id
        extra_context['code'] = train.code or ""

        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['show_save_and_add_another'] = False
        return super(PythonTrainAdmin, self).change_view(request, object_id, form_url=form_url,
                                                         extra_context=extra_context)

    def add_view(self, request, form_url="", extra_context=None):
        user = request.user
        self.change_form_template = "python_train/change_form.html"
        extra_context = extra_context or {}
        extra_context['user'] = user
        extra_context['sid'] = ""
        extra_context['code'] = ""

        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['show_save_and_add_another'] = False
        return super(PythonTrainAdmin, self).add_view(request, form_url=form_url,
                                                      extra_context=extra_context)


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectFiles, ProjectFilesAdmin)
admin.site.register(PythonTrain, PythonTrainAdmin)
