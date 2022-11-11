from django.contrib import admin

from .models import JwtToken


@admin.register(JwtToken)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['get_expiration', 'token', 'created_at']
    list_display_links = ['get_expiration', 'token']
    readonly_fields = ('token',)

    def get_expiration(self, obj):
        return f'ვალიდურია {obj.expiration} დღე'

    get_expiration.short_description = 'ვადა'
