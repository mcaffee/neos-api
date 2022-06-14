from django.contrib import admin

from classifier.models import ClassifierModel


@admin.register(ClassifierModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'training_status', )
