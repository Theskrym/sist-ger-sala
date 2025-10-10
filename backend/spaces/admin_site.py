from django.contrib.admin import AdminSite
from django.template.defaultfilters import register

class SalaAdminSite(AdminSite):
    site_header = 'Sistema de Gerenciamento de Salas'
    site_title = 'Portal Administrativo CESMAC'
    index_title = 'Gerenciamento'
    
    def each_context(self, request):
        context = super().each_context(request)
        context.update({
            'has_permission': True,
            'is_popup': False,
            'is_nav_sidebar_enabled': True,
        })
        return context

admin_site = SalaAdminSite(name='sala_admin')