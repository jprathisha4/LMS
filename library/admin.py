from django.contrib import admin
from .models import Book,StudentExtra,IssuedBook, Genre, LibrarySetting
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book, BookAdmin)


@admin.register(LibrarySetting)
class LibrarySettingAdmin(admin.ModelAdmin):
    list_display = ['expiry_days', 'fine_per_day','brand_name','logo']

    
class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)


class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'status', 'fine_display', 'expiry_date', 'fine_per_day', 'custom_expiry_days')
    list_editable = ('fine_per_day', 'custom_expiry_days')

    def fine_display(self, obj):
        return obj.get_display_fine()
    fine_display.short_description = 'Fine'
admin.site.register(IssuedBook, IssuedBookAdmin)



class GenreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Genre, GenreAdmin)

