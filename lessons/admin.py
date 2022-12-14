from django.utils.html import format_html, mark_safe
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from common.utils import logger
from lessons.models import Course, Lesson, Exercises, Homework, Attendance


class LessonFilter(admin.SimpleListFilter):
    title = _('课程', )
    parameter_name = "lesson"

    def lookups(self, request, model_admin):
        return [(i.id, _(i.course.title if i.course else str(i.id))) for i in Lesson.objects.filter(is_deleted=0)]

    def queryset(self, request, queryset):
        queryset = queryset.filter(is_deleted=0)
        return queryset


class ExercisesFilter(admin.SimpleListFilter):
    title = _('习题', )
    parameter_name = "exercises"

    def lookups(self, request, model_admin):
        return [(i.id, _(i.title)) for i in Exercises.objects.filter(is_deleted=0)]

    def queryset(self, request, queryset):
        queryset = queryset.filter(is_deleted=0)
        return queryset


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created')
    search_fields = ('title',)
    exclude = ('is_deleted',)
    sortable_by = ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(is_deleted=0)
        return qs

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'need_code', 'need_answer')
    exclude = ('is_deleted',)
    sortable_by = ()

    def get_queryset(self, request):
        qs = super(ExercisesAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        return qs

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


from lessons.views import lesson_list_page


class LessonAdmin(admin.ModelAdmin):
    # list_display = ('id', 'grade', 'num', 'title', 'lesson_date')
    # search_fields = ('titles',)
    # list_filter = ('grade', 'num')
    exclude = ('is_deleted',)
    # actions_selection_counter = False
    # sortable_by = ()
    filter_horizontal = ('user', 'exercises')
    # show_full_result_count = False
    #
    # def title(self, obj):
    #     return format_html(obj.course.title)
    #
    # title.short_description = "名称"
    #
    # def grade_name(self, obj):
    #     qs = Lesson.objects.filter(lesson_id=obj.id, is_deleted=0).values_list('name', flat=True)
    #     res = '<br/>'.join(list(qs))
    #     return format_html(res)
    #
    # grade_name.short_description = "班级"
    #
    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super(LessonAdmin, self).get_search_results(request, queryset, search_term)
    #     try:
    #         queryset &= (self.model.objects.filter(course__title__icontains=search_term))
    #     except:
    #         pass
    #     return queryset, use_distinct
    #
    # def get_queryset(self, request):
    #     qs = super(LessonAdmin, self).get_queryset(request)
    #     # qs = qs.filter(is_deleted=0)
    #     if not request.user.is_superuser:
    #         qs = qs.filter(grade_id=request.user.grade_id, status=1).order_by('-num')
    #     return qs
    #
    # def changelist_view(self, request, extra_context=None):
    #     if not request.user.is_superuser:
    #         self.list_display = ('num', 'title', 'lesson_date')
    #         self.list_display_links = ('title',)
    #         self.search_fields = ('title',)
    #         self.list_filter = ('num',)
    #     return super(LessonAdmin, self).changelist_view(request, extra_context=extra_context)
    #
    def change_view(self, request, object_id, form_url="", extra_context=None):
        user = request.user
        if not user.is_superuser:
            self.change_form_template = "lessons/change_form.html"
            extra_context = extra_context or {}
            lesson = Lesson.objects.filter(id=object_id).first()
            extra_context['lesson'] = lesson
            extra_context['user'] = user
        return super(LessonAdmin, self).change_view(request, object_id, form_url=form_url,
                                                    extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        return lesson_list_page(request)

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


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'lesson_title', 'exercises_title', 'comment_content', 'created')
    exclude = ('is_deleted',)
    sortable_by = ()
    list_filter = (LessonFilter, 'user', ExercisesFilter)
    actions_selection_counter = False
    # raw_id_fields = ('user', 'lesson', 'exercises')
    fields = ('user', 'lesson', 'exercises', 'code', 'content', 'comment')
    # readonly_fields = ('user', 'lesson', 'exercises')
    view_on_site = False

    def user_name(self, obj):
        return format_html(obj.user.name)

    user_name.short_description = "学生姓名"

    def lesson_title(self, obj):
        return format_html(obj.lesson.course.title)

    lesson_title.short_description = "课程名称"

    def exercises_title(self, obj):
        return format_html(obj.exercises.title)

    exercises_title.short_description = "作业名称"

    def comment_content(self, obj):
        return format_html(obj.comment or "")

    comment_content.short_description = "老师评语"

    def get_queryset(self, request):
        qs = super(HomeworkAdmin, self).get_queryset(request)
        qs = qs.filter(is_deleted=0)
        if not request.user.is_superuser:
            qs = qs.filter(user_id=request.user.id)
        return qs

    def homework_title(self, obj):
        return obj.lesson.title if obj.lesson else ''

    homework_title.short_description = '作业名称'

    def created_name(self, obj):
        return obj.created

    created_name.short_description = "保存时间"

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


from lessons.views import attendance_list_page


class AttendanceAdmin(admin.ModelAdmin):
    pass

    def changelist_view(self, request, extra_context=None):
        return attendance_list_page(request)

    def has_module_permission(self, request):
        return True


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Exercises, ExercisesAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Attendance, AttendanceAdmin)
