from django.contrib import admin

from board.models import Board


# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title','username','create_at')

admin.site.register(Board, BoardAdmin)