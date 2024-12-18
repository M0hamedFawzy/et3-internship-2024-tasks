from django.contrib import admin, messages
from app.models import *
from django.db import IntegrityError
from django.db import transaction


admin.site.site_header = 'كلمات كاش'
admin.site.index_title = 'كلمات كاش'
admin.site.site_title = 'كلمات كاش'

#admin.site.register(حساب)
#admin.site.register(تحويل)
# admin.site.register(شحن)
# admin.site.register(سحب)
admin.site.register(فرع)
admin.site.register(موظف)

@ admin.register(حساب)
class حسابAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # return qs.filter(user__groups__user=request.user)
        return qs.filter(المالك=request.user)
    list_display=('المالك','الرصيد')

@ admin.register(تحويل)
class تحويلAdmin(admin.ModelAdmin):


    list_display=('من','إلى','المبلغ')
    def save_model(self, request, obj, form, change):
            try:
                with transaction.atomic():
                    super().save_model(request, obj, form, change)
            except (IntegrityError, ValueError):
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'الرصيد لا يكفي')
                return None

@ admin.register(شحن)
class شحنAdmin(admin.ModelAdmin):


    list_display=('الفرع','لصالح','المبلغ')
    fields=('لصالح','المبلغ')

    def save_model(self, request, obj, form, change):
        obj.الفرع = request.user.موظف.الفرع
        super().save_model(request, obj, form, change)

@ admin.register(سحب)
class سحبAdmin(admin.ModelAdmin):


    list_display=('الفرع','لصالح','المبلغ')
    fields=('لصالح','المبلغ')

    def save_model(self, request, obj, form, change):

        try:
            with transaction.atomic():
                obj.الفرع = request.user.موظف.الفرع
                super().save_model(request, obj, form, change)
        except (IntegrityError, ValueError):
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'الرصيد لا يكفي')
            return None
        