import json
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import SaveState


class PrettyJSONWidget(forms.Textarea):
    """Textarea widget formatted with a monospace font for JSON editing."""
    def __init__(self, attrs=None):
        default_attrs = {
            'rows': 25,
            'cols': 90,
            'style': 'font-family: monospace; font-size: 13px; width: 95%; background-color: #f8f9fa;',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class PrettyJSONFormField(forms.JSONField):
    """JSONField that indents JSON for clean, readable editing in Django admin."""
    widget = PrettyJSONWidget

    def prepare_value(self, value):
        if isinstance(value, forms.fields.InvalidJSONInput):
            return value
        return json.dumps(value, ensure_ascii=False, indent=2, cls=self.encoder)


class SaveStateAdminForm(forms.ModelForm):
    state = PrettyJSONFormField(
        help_text="Game save state in JSON format. Validated automatically upon save."
    )

    class Meta:
        model = SaveState
        fields = '__all__'


@admin.register(SaveState)
class SaveStateAdmin(admin.ModelAdmin):
    form = SaveStateAdminForm
    list_display = ('user', 'updated_at', 'get_screen', 'get_gold', 'get_party_members')
    list_filter = ('updated_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('updated_at',)
    ordering = ('-updated_at',)

    @admin.display(description='Current Screen')
    def get_screen(self, obj):
        return obj.state.get('screen', '—') if isinstance(obj.state, dict) else '—'

    @admin.display(description='Party Gold')
    def get_gold(self, obj):
        if isinstance(obj.state, dict):
            return obj.state.get('party', {}).get('gold', '—')
        return '—'

    @admin.display(description='Party Members')
    def get_party_members(self, obj):
        if isinstance(obj.state, dict):
            members = obj.state.get('party', {}).get('members', [])
            return ", ".join(m.get('name', 'Unknown') for m in members) or 'None'
        return '—'


class SaveStateInline(admin.StackedInline):
    """Allows viewing and editing SaveState directly inside the User admin change page."""
    model = SaveState
    form = SaveStateAdminForm
    can_delete = False
    verbose_name_plural = 'Save State'
    readonly_fields = ('updated_at',)


# Re-register UserAdmin to include SaveState inline on the User page
class UserAdmin(BaseUserAdmin):
    inlines = [SaveStateInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
