from django.utils.html import format_html, mark_safe
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from common.utils import logger
from lessons.models import LessonType, LessonTypeUser, Lesson, Homework, LessonHomework, HomeworkSubject, LessonUser


class LessonTypeFilter(admin.SimpleListFilter):
    title = _("课程分类", )
    parameter_name = "lesson_type"

    def lookups(self, request, model_admin):
        return [(i.id, _(i.name)) for i in LessonType.objects.filter(is_deleted=0)]

    def queryset(self, request, queryset):
        queryset = queryset.filter(is_deleted=0)
        return queryset


class LessonFilter(admin.SimpleListFilter):
    title = _('课程', )
    parameter_name = "lesson"

    def lookups(self, request, model_admin):
        return [(i.id, _(i.title)) for i in Lesson.objects.filter(is_deleted=0)]

    def queryset(self, request, queryset):
        queryset = queryset.filter(is_deleted=0)
        return queryset


class HomeworkSubjectFilter(admin.SimpleListFilter):
    title = _('习题', )
    parameter_name = "homework_subject"

    def lookups(self, request, model_admin):
        return [(i.id, _(i.title)) for i in HomeworkSubject.objects.filter(is_deleted=0)]

    def queryset(self, request, queryset):
        queryset = queryset.filter(is_deleted=0)
        return queryset


class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    exclude = ('is_deleted',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def get_queryset(self, request):
        qs = super(LessonTypeAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        return qs


class LessonTypeUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lesson_type')
    exclude = ('is_deleted',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def get_queryset(self, request):
        qs = super(LessonTypeUserAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        return qs


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title_name', 'lesson_type_name')
    list_display_links = ('title_name',)
    search_fields = ('title',)
    exclude = ('is_deleted',)
    list_filter = (LessonTypeFilter,)
    actions_selection_counter = False
    sortable_by = ()

    def lesson_type_name(self, obj):
        return obj.lesson_type.name or ""

    lesson_type_name.short_description = "课程阶段"

    def title_name(self, obj):
        return mark_safe(obj.title or "")

    title_name.short_description = "课程"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if request.user.is_superuser:
            return super(LessonAdmin, self).change_view(request, object_id, form_url=form_url,
                                                        extra_context=extra_context)
        else:
            self.change_form_template = "lessons/change_form.html"

            extra_context = extra_context or {}
            lesson = Lesson.objects.filter(id=object_id).first()
            extra_context['lesson'] = lesson
            h = HomeworkSubject.objects.filter(lessonhomework__lesson_id=object_id).first()
            data = {'id': h.id, 'title': h.title, 'content': h.content, 'default_code': h.default_code}
            homework = Homework.objects.filter(user_id=request.user.id, is_deleted=0,
                                               homework_subject_id=h.id).first()
            default_code = format_html(homework.code) if homework and homework.code else format_html(
                data.get('default_code', ''))
            default_code.replace("'", "\'").replace('"', '\"')
            logger.info(default_code)
            data['default_code'] = default_code
            extra_context['homework_subject'] = data
            return super(LessonAdmin, self).change_view(request, object_id, form_url=form_url,
                                                        extra_context=extra_context)

    def get_queryset(self, request):
        qs = super(LessonAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
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


class HomeworkSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')
    exclude = ('is_deleted',)

    def get_queryset(self, request):
        qs = super(HomeworkSubjectAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        return qs

    def has_module_permission(self, request):
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

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class LessonHomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'homework_subject')
    exclude = ('is_deleted',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def get_queryset(self, request):
        qs = super(LessonHomeworkAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        return qs


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'homework_subject', 'comment', 'created')
    exclude = ('is_deleted',)
    sortable_by = ()
    list_filter = (HomeworkSubjectFilter,)
    actions_selection_counter = False

    def get_queryset(self, request):
        qs = super(HomeworkAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        if not request.user.is_superuser:
            qs = qs.filter(user_id=request.user.id)
        return qs

    def homework_title(self, obj):
        return obj.homework_subject.title if obj.homework_subject else ''

    homework_title.short_description = '作业名称'

    def created_name(self, obj):
        return obj.created

    created_name.short_description = "保存时间"

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.list_display = ('homework_title', 'created_name')
            self.exclude = ('is_deleted', 'user')
        return super(HomeworkAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if request.user.is_superuser:
            return super(HomeworkAdmin, self).change_view(request, object_id, form_url=form_url,
                                                          extra_context=extra_context)
        else:
            self.change_form_template = "homework/change_form.html"
            extra_context = extra_context or {}
            homework = Homework.objects.filter(id=object_id).first()
            subject = homework.homework_subject if homework else None
            extra_context['homework_subject'] = subject
            code = format_html(homework.code) if homework else ""
            code.replace("'", "\'").replace('"', '\"')
            extra_context['code'] = code
            logger.info(extra_context)
            extra_context['comment'] = format_html(homework.comment) if homework and homework.comment else ""
            return super(HomeworkAdmin, self).change_view(request, object_id, form_url=form_url,
                                                          extra_context=extra_context)

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


class LessonUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson_name', 'user_name', 'lesson_date')
    exclude = ('is_deleted',)
    list_filter = ('user', 'lesson')
    sortable_by = ()
    actions_selection_counter = False

    def get_list_filter(self, request):
        res = super(LessonUserAdmin, self).get_list_filter(request)
        print(res)
        if request.user.is_superuser:
            res = ('user', LessonFilter)
        else:
            res = (LessonFilter,)
        return res

    def lesson_name(self, obj):
        return format_html(obj.lesson.title)

    lesson_name.short_description = "课程"

    def user_name(self, obj):
        return format_html(obj.user.name)

    user_name.short_description = "姓名"

    def get_queryset(self, request):
        qs = super(LessonUserAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        if not request.user.is_superuser:
            qs = qs.filter(user_id=request.user.id)
        return qs

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


admin.site.register(LessonType, LessonTypeAdmin)
admin.site.register(LessonTypeUser, LessonTypeUserAdmin)
admin.site.register(HomeworkSubject, HomeworkSubjectAdmin)
admin.site.register(LessonHomework, LessonHomeworkAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonUser, LessonUserAdmin)
