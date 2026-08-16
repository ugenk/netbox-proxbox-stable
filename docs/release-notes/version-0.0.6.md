# Version 0.0.6

Tested with NetBox **v4.6.8** and Proxmox up to **8.4**.

## Compatibility

* NetBox 4.x support (serializers, `ChangeLoggedModel` import, plugin API)
* Removed FastAPI / async backend from this stable fork
* Multi-Proxmox endpoint support
* `BASE_PATH` support for NetBox behind a URL prefix

## Features

* `node_name_with_cluster` setting: optionally prefix NetBox device names with the cluster name

## Fixes

* Virtual machine detail pages no longer query `netbox_proxbox_proxmoxvm` via reverse ForeignKey (`related_name='+'`)
* Migration `0004` aligns `created` (`DateTimeField`) and `id` (`BigAutoField`) with NetBox 4.6
* `single_update` no longer crashes when a VM interface has no MAC address
* Credentials (password, token, cluster IP) are no longer exposed without authorization

## Upgrade notes

Apply plugin migrations after install:

```bash
python3 manage.py migrate netbox_proxbox
```

If `showmigrations netbox_proxbox` shows all migrations as applied (`[X]`), but PostgreSQL has no table `netbox_proxbox_proxmoxvm`:

```bash
python3 manage.py migrate netbox_proxbox zero --fake
python3 manage.py migrate netbox_proxbox
```
