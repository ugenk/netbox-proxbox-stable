from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
# 'View' is a django subclass. Basic type of class-based views
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.views.decorators.cache import never_cache

# Enables permissions for views using Django authentication system.
# PermissionRequiredMixin = will handle permission checks logic and will plug into the
# Netbox's existing authorization system.
# TODO: check all that permissions stuff
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .icon_classes import icon_classes
from .filters import ProxmoxVMFilter
from .forms import ProxmoxVMForm, ProxmoxVMFilterForm
from .models import ProxmoxVM
from .tables import ProxmoxVMTable, VMUpdateResult, NodeUpdateResult

from netbox_proxbox import proxbox_api
import json

from netbox import configuration

from . import ProxboxConfig

import markdown
from . import github


class HomeView(LoginRequiredMixin, View):
    """Homepage"""
    template_name = 'netbox_proxbox/home.html'

    # service incoming GET HTTP requests
    def get(self, request):
        """Get request."""

        plugin_configuration = configuration.PLUGINS_CONFIG
        default_config = ProxboxConfig.default_settings

        return render(
            request,
            self.template_name,
            {
                "configuration": plugin_configuration,
                "default_config": default_config,
                "configuration_json": json.dumps(plugin_configuration, indent=4),
                "default_config_json": json.dumps(default_config, indent=4)
            }
        )


class ContributingView(View):
    """Contributing"""
    template_name = 'netbox_proxbox/contributing.html'

    # service incoming GET HTTP requests
    def get(self, request):
        """Get request."""

        title = "Contributing to Proxbox Project"

        return render(
            request,
            self.template_name,
            {
                "html": github.get(filename="CONTRIBUTING.md"),
                "title": title,
            }
        )


class CommunityView(View):
    """Community"""
    template_name = 'netbox_proxbox/community.html'

    # service incoming GET HTTP requests
    def get(self, request):
        """Get request."""

        title = "Join our Community!"

        return render(
            request,
            self.template_name,
            {
                "title": title,
            }
        )


def DiscussionsView(request):
    external_url = "https://github.com/orgs/netdevopsbr/discussions"
    return redirect(external_url)


def DiscordView(request):
    external_url = "https://discord.com/invite/9N3V4mpMXU"
    return redirect(external_url)


def TelegramView(request):
    external_url = "https://t.me/netboxbr"
    return redirect(external_url)


class ProxmoxSingleUpdate(PermissionRequiredMixin, View):
    """Update a single Proxmox information on Netbox."""

    # Define permission
    permission_required = "netbox_proxbox.view_proxmoxvm"

    # service incoming POST HTTP requests
    # 'proxmox_domain' value is passed to post()
    def post(self, request):
        """Post request."""

        proxmox_domain = self.request.POST.get('proxmox_domain')
        json_result = proxbox_api.update.single(remove_unused=True, proxmox_domain=proxmox_domain)

        return render(
            request,
            "netbox_proxbox/proxmox_vm_full_update.html",
            {
                "proxmox": json_result,
                "proxmox_json": json.dumps(json_result, indent=4)
            },
        )


class ProxmoxFullUpdate(PermissionRequiredMixin, View):
    """Full Update of Proxmox information on Netbox."""

    # Define permission
    permission_required = "netbox_proxbox.view_proxmoxvm"

    # service incoming GET HTTP requests
    # 'pk' value is passed to get() via URL defined in urls.py
    def get(self, request):
        """Get request."""

        json_result = proxbox_api.update.all(remove_unused=True)

        return render(
            request,
            "netbox_proxbox/proxmox_vm_full_update.html",
            {
                "proxmox": json_result,
                "proxmox_json": json.dumps(json_result, indent=4)
            },
        )


class ProxmoxVMView(PermissionRequiredMixin, View):
    """Display Virtual Machine details"""

    # specify permission required to access the view
    permission_required = "netbox_proxbox.view_proxmoxvm"

    # retrieve and filter objects on ProxmoxVM
    queryset = ProxmoxVM.objects.all()

    # service incoming GET HTTP requests
    # 'pk' value is passed to get() via URL defined in urls.py
    def get(self, request, pk):
        """Get request."""

        # get_object_or_404() returns 404 HTML code instead of raising internal exception
        # pk = primary key
        proxmoxvm_obj = get_object_or_404(self.queryset, pk=pk)

        # render() renders provided template and uses it to create a well-formed web response
        return render(
            request,
            "netbox_proxbox/proxmox_vm.html",
            {
                "proxmoxvm": proxmoxvm_obj,
            },
        )


class ProxmoxVMListView(PermissionRequiredMixin, View):
    """View for listing all existing Virtual Machines."""

    permission_required = "netbox_proxbox.view_proxmoxvm"

    # all of the objects should be given to the view
    queryset = ProxmoxVM.objects.all()

    filterset = ProxmoxVMFilter

    # form that will be rendered in list view template
    filterset_form = ProxmoxVMFilterForm

    def get(self, request):
        """Get request."""

        # where the filtering happens.
        # the filterset is fed with form values contained in request.GET and queryset with ProxmoxVM objects.
        # '.qs' = returns QuerySet like object what is assigned back to 'self.queryset'
        # the 'self.queryset' is then fed to table constructor
        self.queryset = self.filterset(request.GET, self.queryset).qs

        # table class

        table = ProxmoxVMTable(self.queryset)

        # RequestConfig is used to configure pagination of 25 object per page
        # RequestConfig(request, paginate={"per_page": 25}).configure(table)

        return render(
            request, "netbox_proxbox/proxmox_vm_list.html",
            {
                "table": table,
                "filter_form": self.filterset_form(request.GET),
                "icon_classes": icon_classes,
            }
        )


# 'CreateView' is provided by Django
class ProxmoxVMCreateView(PermissionRequiredMixin, CreateView):
    """View for creating a new ProxmoxVM instance."""

    permission_required = "netbox_proxbox.add_proxmoxvm"

    form_class = ProxmoxVMForm
    template_name = "netbox_proxbox/proxmox_vm_edit.html"


class ProxmoxVMDeleteView(PermissionRequiredMixin, DeleteView):
    """View for deleting ProxmoxVM instance."""

    permission_required = "netbox_proxbox.delete_proxmoxvm"

    model = ProxmoxVM
    # reverse_lazy = function used to return the page for the given namespace URL
    # success_url = which view will redirect after an object has been deleted
    success_url = reverse_lazy("plugins:netbox_proxbox:proxmoxvm_list")

    # template_name = points to the template that will be rendred when asked to confirm the deletion
    template_name = "netbox_proxbox/proxmox_vm_delete.html"


class ProxmoxVMEditView(PermissionRequiredMixin, UpdateView):
    """View for editing a ProxmoxVM instance."""

    permission_required = "netbox_proxbox.change_proxmoxvm"

    model = ProxmoxVM
    form_class = ProxmoxVMForm
    template_name = "netbox_proxbox/proxmox_vm_edit.html"
