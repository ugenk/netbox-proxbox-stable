# base serializer class
from rest_framework import serializers

# NetBox 4.2+: nested serializers removed; use primary serializers with nested=True
from virtualization.api.serializers import ClusterSerializer, VirtualMachineSerializer

# model that will be built the serializer
from netbox_proxbox.models import ProxmoxVM


class ProxmoxVMSerializer(serializers.ModelSerializer):
    """Serializer for the ProxmoxVM model."""

    cluster = ClusterSerializer(
        nested=True,
        # set relationship type to many-to-one
        many=False,
        # the field is allowed as the input in API calls
        read_only=False,
        # specifies whether field is required.
        # it must follow the corresponding property set for the model field
        required=False,
        help_text="ProxmoxVM Cluster"
    )

    virtual_machine = VirtualMachineSerializer(
        nested=True,
        many=False,
        read_only=False,
        required=True,
        help_text="ProxmoxVM Virtual Machine"
    )

    class Meta:
        model = ProxmoxVM
        fields = [
            "id",
            "cluster",
            "virtual_machine",
            "proxmox_vm_id",
            "status",
            "node",
            "vcpus",
            "memory",
            "disk",
            "type",
            "description",
        ]
