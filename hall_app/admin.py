from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .forms import SeatCreationForm, SectionSeatCreationForm
from .models import Hall, Sector, Line, Section, Seat


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    fields = ['line', 'section', 'number']
    show_change_link = True

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
    list_per_page = 10


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hall', 'created_at', 'updated_at')
    list_filter = ('hall', 'created_at', 'updated_at')
    search_fields = ('name', 'hall__name')
    exclude = ('is_active',)  # is_active maydonini yashirish
    inlines = [SectionInline, LineInline]
    list_per_page = 10


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('number', 'sector', 'created_at', 'updated_at')
    list_filter = ('sector', 'created_at', 'updated_at')
    search_fields = ('number', 'sector__name')
    exclude = ('is_active',)  # is_active maydonini yashirish
    actions = ['create_seats_in_section']
    inlines = [SeatInline]
    list_per_page = 20

    def create_seats_in_section(self, request, queryset):
        # Agar checkbox orqali tanlangan bo'lsa, querysetni yangilash
        if request.POST.get(ACTION_CHECKBOX_NAME):
            selected_ids = request.POST.getlist(ACTION_CHECKBOX_NAME)
            queryset = Section.objects.filter(pk__in=selected_ids)

        if queryset.count() != 1:
            self.message_user(request, "Iltimos, faqat bitta bo'limni tanlang!", level="error")
            return

        section = queryset.first()
        form = SectionSeatCreationForm(request.POST or None, section=section)

        if 'apply' in request.POST:
            if form.is_valid():
                start_seat = form.cleaned_data['start_seat']
                end_seat = form.cleaned_data['end_seat']
                line = form.cleaned_data['line']

                # O'rindiqlarni yaratish
                section.create_seats_in_section(start_seat=start_seat, end_seat=end_seat, line=line)
                self.message_user(request, f"{start_seat} dan {end_seat} gacha o‘rindiqlar yaratildi.")
                return

        return render(
            request,
            'admin/create_seats_in_section_form.html',
            {
                'form': form,
                'section': section,
                'queryset': queryset,
                'action_checkbox_name': ACTION_CHECKBOX_NAME,
            },
        )

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions = {
            key: (value[0], _(value[1]), value[2])
            for key, value in actions.items()
        }
        return actions

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create_seats_in_section/', self.create_seats_in_section_view),
        ]
        return custom_urls + urls

    def create_seats_in_section_view(self, request):
        return HttpResponse("O'rindiq yaratish tugmasi ishlaydi!")


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('sector', 'number', 'created_at')
    list_filter = ('sector', 'created_at', 'updated_at')
    search_fields = ('number', 'sector__name')
    exclude = ('is_active',)  # is_active maydonini yashirish
    actions = ['create_seats_action']
    inlines = [SeatInline]
    list_per_page = 20

    def create_seats_action(self, request, queryset):
        if request.POST.get(ACTION_CHECKBOX_NAME):
            selected_ids = request.POST.getlist(ACTION_CHECKBOX_NAME)
            queryset = self.model.objects.filter(pk__in=selected_ids)

        if queryset.count() != 1:
            self.message_user(request, "Iltimos, faqat bitta qator tanlang!", level="error")
            return

        line = queryset.first()
        form = SeatCreationForm(request.POST or None)

        if 'apply' in request.POST:
            if form.is_valid():
                start_seat = form.cleaned_data['start_seat']
                end_seat = form.cleaned_data['end_seat']
                section = form.cleaned_data['section']
                line.create_seats(start_seat=start_seat, end_seat=end_seat, section=section)
                self.message_user(request, f"{start_seat} dan {end_seat} gacha o‘rindiqlar yaratildi.")
                return

        return render(
            request,
            'admin/create_seats_form.html',
            {
                'form': form,
                'line': line,
                'queryset': queryset,
                'action_checkbox_name': ACTION_CHECKBOX_NAME,
            },
        )

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions = {
            key: (value[0], _(value[1]), value[2])
            for key, value in actions.items()
        }
        return actions

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create_seats/', self.create_seats_view),
        ]
        return custom_urls + urls

    def create_seats_view(self, request):
        # Bu yerda forma va tugma bilan bog'liq qo'shimcha logika bo'lishi mumkin
        return HttpResponse("Qo'shimcha tugma ishlaydi!")


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('line__sector__name', 'line__number', 'section__number', 'number')
    list_filter = ('line__sector__hall', 'line__sector', 'line', 'section')
    search_fields = ('number', 'line__number', 'section__number')
    exclude = ('is_active',)  # is_active maydonini yashirish
    list_per_page = 50
