from django.contrib import admin
from pybo.models import Question, Answer

# Register your models here.
admin.register(Question)
admin.site.register(Answer)

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)


