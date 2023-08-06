# Django
from django.views.generic import TemplateView
from django.conf import settings
from django.urls import reverse
from django.contrib import messages

# Mixins
from hydra.base.mixins import BreadcrumbMixin, UrlMixin, TemplateMixin
from hydra.shortcuts import get_urls_of_site


class ModuleView(TemplateView):
    """Clase para definir las vistas de los módulos de aplicaciones"""

    def get_template_names(self):
        template_name = "hydra/module_list.html"
        if hasattr(settings, "MODULE_TEMPLATE_NAME"):
            template_name = settings.MODULE_TEMPLATE_NAME
        return [template_name]


def get_base_view(View, Mixin, site):
    class View(BreadcrumbMixin, UrlMixin, TemplateMixin, Mixin, View):
        def form_valid(self, form):
            messages.success(self.request, "Se ha guardado correctamente.")
            return super().form_valid(form)

        def get_success_url(self):
            return get_urls_of_site(self.site).get(f"{self.site.success_url}_url")

    View.site = site
    View.model = site.model
    return View

    #
    # def has_permission(self):
    #     return False
    #     ctx = super().get_context_data(self.request.kwargs)
    #     print(ctx)
    #     user = self.request.user
    #     permissions = list()
    #     for model in ctx["models_permissions"]:
    #         permissions.append(f"{model._meta.app_label}.view_{model._meta.model_name}")
    #     return any(user.has_perm(permission) for permission in permissions)

