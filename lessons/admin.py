from django.contrib import admin
from lessons.models import LessonType, Lesson, Homework, LessonHomework, HomeworkSubject


class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    exclude = ('is_deleted',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_type_name', 'title_name')
    list_display_links = ('title_name',)
    exclude = ('is_deleted',)
    sortable_by = ()
    # list_filter = ('lesson_type',)

    def lesson_type_name(self, obj):
        return obj.lesson_type

    lesson_type_name.short_description = "课程阶段"

    def title_name(self, obj):
        return obj.title

    title_name.short_description = "课程"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if request.user.is_superuser:
            return super(LessonAdmin, self).change_view(request, object_id, form_url=form_url,
                                                        extra_context=extra_context)
        else:
            self.change_form_template = "lessons/change_form.html"
            self.readonly_fields = ('lesson_type',)
            self.exclude = ('is_deleted', 'sort')
            extra_context = extra_context or {}
            lesson = Lesson.objects.filter(id=object_id).first()
            extra_context['lesson'] = lesson
            extra_context['homework_subjects'] = HomeworkSubject.objects.filter(lessonhomework__lesson_id=object_id)
            return super(LessonAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

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

    def has_module_permission(self, request):
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


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'homework_subject', 'created')
    exclude = ('is_deleted',)
    sortable_by = ()

    def get_queryset(self, request):
        qs = super(HomeworkAdmin, self).get_queryset(request)
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
        homework = Homework.objects.filter(id=object_id).first()
        subject = homework.homework_subject if homework else None
        extra_context['homework_subject'] = subject
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


admin.site.register(LessonType, LessonTypeAdmin)
admin.site.register(HomeworkSubject, HomeworkSubjectAdmin)
admin.site.register(LessonHomework, LessonHomeworkAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Lesson, LessonAdmin)
