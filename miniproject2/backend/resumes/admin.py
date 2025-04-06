from django.contrib import admin

from resumes.models import Resume


class ResumeInline(admin.TabularInline):
    model = Resume
    extra = 1
    fields = ('title', 'file', 'processed')
    readonly_fields = ('processed',)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at', 'processed', 'file_link')
    list_filter = ('processed', 'uploaded_at', 'user__role')
    search_fields = ('title', 'user__username')
    readonly_fields = ('uploaded_at', 'extracted_data', 'processed')

    def file_link(self, obj):
        if obj.file:
            return f'<a href="{obj.file.url}" target="_blank">Download</a>'
        return "No file"
    file_link.allow_tags = True
    file_link.short_description = "File"