from django.contrib import admin
from .models import Post, Profile, Comment,Images


def make_published(modeladmin, request, queryset):
    queryset.update(status='published')


make_published.short_description = "Mark selected stories as published"


def make_draft(modeladmin, request, queryset):
    queryset.update(status='draft')


make_draft.short_description = "Mark selected stories as draft"


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status')
    list_filter = ('status', 'date_posted')
    search_fields = ('author__username', 'title')
    list_editable = ('status',)
    date_hierarchy = ('date_posted')
    actions = [make_published, make_draft]


admin.site.register(Profile)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Images)

