from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from .models import Product, City, Country, Element, ProductName

# Register your models here.

User = get_user_model()
admin.site.register(Product)
admin.site.register(City)
admin.site.register(Country)
# admin.site.register(Worker)
admin.site.register(ProductName)
admin.site.register(User)
from  .tasks import update_queryset

@admin.register(Element)
class MembersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'debt', 'city', 'link')

    # search_fields = ('title', 'date')
    # print(Member.objects.get(provider__member__id=1))

    list_filter = ('city',)
    actions = ('clean_debt', 'make_dist')

    @admin.display(description='Povider')
    def link(self, member: Element):
        if member.provider:
            return mark_safe(f"""
            <a href="/admin/electronicsSales/element/{member.provider.id}/change/" target="_blank">{member.provider.name}</a>
            """)

    @admin.display(description='Очистить задолжность')
    def clean_debt(self, request, queryset):
        print(request, queryset)
        if len(queryset) > 20:
            print('go to task clean')
            for q in queryset:
                update_queryset.delay(q.id)
        else:
            queryset.update(debt=0)

    @admin.display(description='сделать дистрибьютером')
    def make_dist(self, request, queryset):
        print(request, queryset)
        queryset.update(type=Element.DISTRIBUTOR)
