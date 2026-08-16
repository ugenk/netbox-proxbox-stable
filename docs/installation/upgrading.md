# Upgrading ProxBox

## 0.0.6

1. Install the new plugin version.
2. Apply database migrations:

```bash
cd /opt/netbox/netbox/
python3 manage.py migrate netbox_proxbox
python3 manage.py collectstatic --no-input
```

If `showmigrations netbox_proxbox` shows all migrations as applied (`[X]`), but PostgreSQL has no table `netbox_proxbox_proxmoxvm`:

```bash
python3 manage.py migrate netbox_proxbox zero --fake
python3 manage.py migrate netbox_proxbox
```

3. Restart NetBox:

```bash
systemctl restart netbox
```
