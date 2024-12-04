from django.contrib import admin

from .models import Hall, Sector, Line, Section, Seat

class LineInline(admin.TabularInline):
    model = Line
    extra = 0
    fields = ['number']  # Qatorning raqami
    show_change_link = True

class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    fields = ['number']  # Bo'limning raqami
    show_change_link = True


class SectorInline(admin.TabularInline):
    model = Sector
    extra = 0
    fields = ['name', 'section_count', 'line_count']  # Sector nomi va bo'lim va qatorlar soni
    show_change_link = True


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'address', 'description', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'address')
    exclude = ('is_active',)  # is_active maydonini yashirish
    inlines = [SectorInline]


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hall', 'created_at', 'updated_at')
    list_filter = ('hall', 'created_at', 'updated_at')
    search_fields = ('name', 'hall__name')
    exclude = ('is_active',)  # is_active maydonini yashirish
    inlines = [SectionInline, LineInline]


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('number', 'sector', 'created_at', 'updated_at')
    list_filter = ('sector', 'created_at', 'updated_at')
    search_fields = ('number', 'sector__name')
    exclude = ('is_active',)  # is_active maydonini yashirish


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('number', 'sector', 'created_at', 'updated_at')
    list_filter = ('sector', 'created_at', 'updated_at')
    search_fields = ('number', 'sector__name')
    exclude = ('is_active',)  # is_active maydonini yashirish


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('line__sector__name', 'line__number', 'section__number', 'number')
    list_filter = ('line', 'section', 'created_at', 'updated_at')
    search_fields = ('number', 'line__number', 'section__number')
    exclude = ('is_active',)  # is_active maydonini yashirish
