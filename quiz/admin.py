from django.contrib import admin
from .models import Category, Question, Option, QuizAttempt, AttemptAnswer


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4
    min_num = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'time_limit_mins', 'pass_percentage', 'total_questions', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_preview', 'category', 'marks', 'created_at')
    list_filter = ('category', 'marks')
    search_fields = ('text', 'category__name')
    inlines = [OptionInline]

    def text_preview(self, obj):
        return obj.text[:75] + ("..." if len(obj.text) > 75 else "")
    text_preview.short_description = "Question"


class AttemptAnswerInline(admin.TabularInline):
    model = AttemptAnswer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'is_correct', 'marks_obtained')
    can_delete = False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'score', 'total_marks', 'percentage', 'passed', 'time_taken_seconds', 'date_taken')
    list_filter = ('category', 'passed', 'date_taken')
    search_fields = ('user__username', 'category__name')
    readonly_fields = ('user', 'category', 'score', 'total_marks', 'percentage', 'passed', 'time_taken_seconds', 'date_taken')
    inlines = [AttemptAnswerInline]
