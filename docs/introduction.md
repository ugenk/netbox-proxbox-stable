## Netbox Plugin which integrates [Proxmox](https://www.proxmox.com/) and [Netbox](https://netbox.readthedocs.io/)!

This is a fork from original repository [netdevopsbr/netbox-proxbox](https://github.com/netdevopsbr/netbox-proxbox) intended to maintain stable version of proxbox plugin, without FastAPI and async stuff.

Proxbox is currently able to get the following information from Proxmox:

- **Cluster name**
- **Nodes:**
  - Status (online / offline)
  - Name
- **Virtual Machines and Containers:**
  - Status (online / offline)
  - Name
  - ID
  - CPU
  - Disk
  - Memory
  - Node (Server)

---

<div align="center">
	
### Versions

The following table shows the Netbox and Proxmox versions compatible (tested) with Proxbox plugin.

| netbox version   | proxmox version | proxbox version |
|------------------|-----------------|-------------|
| >= v4.1.6        | up to 8.2       | =v0.0.6 |   
| >= v3.4.0        | >= v6.2.0       | =v0.0.5 |
| >= v3.2.0        | >= v6.2.0       | =v0.0.4 |
| >= v3.0.0 < v3.2 | >= v6.2.0       | =v0.0.3 |


</div>

---

### Summary
[1. Installation](#1-installation)
- [1.1. Install package](#11-install-package)
  - [1.1.1. Using pip (production use)](#111-using-pip-production-use---not-working-yet)
  - [1.1.2. Using git (development use)](#112-using-git-development-use)
- [1.2. Enable the Plugin](#12-enable-the-plugin)
- [1.3. Configure Plugin](#13-configure-plugin)
  - [1.3.1. Change Netbox 'configuration.py' to add PLUGIN parameters](#131-change-netbox-configurationpy-to-add-plugin-parameters)
  - [1.3.2. Change Netbox 'settings.py' to include Proxbox Template directory](#132-change-netbox-settingspy-to-include-proxbox-template-directory)
- [1.4. Run Database Migrations](#14-run-database-migrations)
- [1.5 Restart WSGI Service](#15-restart-wsgi-service)

[2. Configuration Parameters](#2-configuration-parameters)

[3. Custom Fields](#3-custom-fields)
- [3.1. Custom Field Configuration](#31-custom-field-configuration)
	- [3.1.1. Proxmox ID](#311-proxmox-id)
	- [3.1.2. Proxmox Node](#312-proxmox-node)
	- [3.1.3. Proxmox Type](#313-proxmox-type-qemu-or-lxc)
	- [3.1.4. Proxmox Keep Interface](#314-proxmox-keep-interface)
- [3.2. Custom Field Example](#32-custom-field-example)

[4. Usage](#4-usage)

[5. Enable Logs](#5-enable-logs)

[6. Contributing](#6-contributing)

[7. Roadmap](#7-roadmap)

[8. Get Help from Community!](#8-get-help-from-community)

---

## 1. Installation

The instructions below detail the process for installing and enabling Proxbox plugin.
The plugin is available as a Python package in pypi and can be installed with pip.

### 1.1. Install package

#### 1.1.1. Using git

Move to netbox main folder
```bash
cd /opt/netbox/netbox
```

Clone netbox-proxbox-stable repository
```bash
git clone https://github.com/ugenk/netbox-proxbox-stable.git
```

Install netbox-proxbox
```bash
cd netbox-proxbox-stable
source /opt/netbox/venv/bin/activate
pip3 install -r requirements.txt && pip3 install .
```

---

### 1.2. Enable the Plugin

Enable the plugin in **/opt/netbox/netbox/netbox/configuration.py**:
```python
PLUGINS = ['netbox_proxbox']
```

---

### 1.3. Configure Plugin

#### 1.3.1. Change Netbox '**[configuration.py](https://github.com/netbox-community/netbox/blob/develop/netbox/netbox/configuration.example.py)**' to add PLUGIN parameters
The plugin's configuration is also located in **/opt/netbox/netbox/netbox/configuration.py**:

Replace the values with your own following the [Configuration Parameters](#2-configuration-parameters) section.

**OBS:** You do not need to configure all the parameters, only the one's different from the default values. It means that if you have some value equal to the one below, you can skip its configuration. For netbox you should ensure the domain/port either targets gunicorn or a true http port that is not redirected to https.

```python
PLUGINS_CONFIG = {
    'netbox_proxbox': {
        'proxmox': [
            {
                'domain': 'proxmox1.example.com',    # May also be IP address
                'http_port': 8006,
                'user': 'root@pam',   # always required
                'password': 'Strong@P4ssword', # only required, if you don't want to use token based authentication
                'token': {
                    'name': 'tokenID',	# Only type the token name and not the 'user@pam:tokenID' format
                    'value': '039az154-23b2-4be0-8d20-b66abc8c4686'
                },
                'ssl': False  # validate ssl cert
            },
            # The following json is optional and applies only for multi-cluster use
            {
                'domain': 'proxmox2.example.com',    # May also be IP address
                'http_port': 8006,
                'user': 'root@pam',   # always required
                'password': 'Strong@P4ssword', # only required, if you don't want to use token based authentication
                'token': {
                    'name': 'tokenID',	# Only type the token name and not the 'user@pam:tokenID' format
                    'value': '039az154-23b2-4be0-8d20-b66abc8c4686'
                },
                'ssl': False  # validate ssl cert
            }
        ],
        'netbox': {
            'domain': 'localhost',     # Ensure localhost is added to ALLOWED_HOSTS
            'http_port': 8001,     # Gunicorn port.
            'token': '0dd7cddfaee3b38bbffbd2937d44c4a03f9c9d38',
            'ssl': False,	# There is no support to SSL on Netbox yet, so let it always False.
            'settings': {
                'virtualmachine_role_id' : 0,
                'node_role_id' : 0,
                'site_id': 0
            }
      }
 }
```

### 1.4. Run Database Migrations

```bash
cd /opt/netbox/netbox/
python3 manage.py migrate
python3 manage.py collectstatic --no-input
```

---

### 1.5. Restart WSGI Service

Restart the WSGI service to load the new plugin:
```bash
systemctl restart netbox
```

---

## 2. Configuration Parameters

The following options are available:

* `proxmox`: (List) Proxmox related configuration to use proxmoxer.
* `proxmox.domain`: (String) Domain or IP address of Proxmox.
* `proxmox.http_port`: (Integer) Proxmox HTTP port (default: 8006).
* `proxmox.user`: (String) Proxmox Username.
* `proxmox.password`: (String) Proxmox Password.
* `proxmox.token`: (Dict) Contains Proxmox TokenID (name) and Token Value (value).
* `proxmox.token.name`: (String) Proxmox TokenID.
* `proxmox.token.value`: (String) Proxmox Token Value.
* `proxmox.ssl`: (Bool) Defines the use of SSL (default: False).

* `netbox`: (Dict) Netbox related configuration to use pynetbox.
* `netbox.domain`: (String) Domain or IP address of Netbox. Ensure name or ip is added to `ALLOWED_HOSTS`
* `netbox.http_port`: (Integer) Netbox HTTP PORT (default: 8001).  If you are not targeting gunicorn directly make sure the HTTP port is not redirected to HTTPS by your HTTP server.
* `netbox.token`: (String) Netbox Token Value.
* `netbox.ssl`: (Bool) Defines the use of SSL (default: False). - Proxbox doesn't support SSL on Netbox yet.
* `netbox.settings`: (Dict) Default items of Netbox to be used by Proxbox. 
  - If not configured, Proxbox will automatically create a basic configuration to make it work.
  - The ID of each item can be easily found on the URL of the item you want to use.
* `netbox.settings.virtualmachine_role_id`: (Integer) Role ID to be used by Proxbox when creating Virtual Machines
* `netbox.settings.node_role_id`: (Integer) Role ID to be used by Proxbox when creating Nodes (Devices)
* `netbox.settings.site_id` (Integer) Site ID to be used by Proxbox when creating Nodes (Devices)

---

## 3. Custom Fields

To get Proxmox ID, Node and Type information, is necessary to configure Custom Fields.
Below the parameters needed to make it work:

### 3.1. Custom Field Configuration

#### 3.1.1. Proxmox ID

Required values (must be equal)
- [Custom Field] **Type:** Integer
- [Custom Field] **Name:** proxmox_id
- [Assignment] **Content-type:** Virtualization > virtual machine
- [Validation Rules] **Minimum value:** 0

Optional values (may be different)
- [Custom Field] **Label:** [Proxmox] ID
- [Custom Field] **Description:** Proxmox VM/CT ID

#### 3.1.2. Proxmox Node

Required values (must be equal)
- [Custom Field] **Type:** Text
- [Custom Field] **Name:** proxmox_node
- [Assignment] **Content-type:** Virtualization > virtual machine

Optional values (may be different)
- [Custom Field] **Label:** [Proxmox] Node
- [Custom Field] **Description:** Proxmox Node (Server)

#### 3.1.3. Proxmox Type (qemu or lxc)

Required values (must be equal)
- [Custom Field] **Type:** Selection
- [Custom Field] **Name:** proxmox_type
- [Assignment] **Content-type:** Virtualization > virtual machine
- [Choices] **Choices:** qemu,lxc

Optional values (may be different)
- [Custom Field] **Label:** [Proxmox] Type
- [Custom Field] **Description:** Proxmox type (VM or CT)

#### 3.1.4. Proxmox Keep Interface

Required values (must be equal)
- [Custom Field] **Type:** Boolean (true/false)
- [Custom Field] **Name:** proxmox_keep_interface
- [Assignment] **Content-type:** DCIM > Interface

### 3.2. Custom Field Example

![custom field image](etc/img/custom_field_example.png?raw=true "preview")

---

## 4. Usage

If everything is working correctly, you should see in Netbox's navigation the **Proxmox VM/CT** button in **Plugins** dropdown list.

On **Proxmox VM/CT** page, click button ![full update button](etc/img/proxbox_full_update_button.png?raw=true "preview")

It will redirect you to a new page and you just have to wait until the plugin runs through all Proxmox Cluster and create the VMs and CTs in Netbox.

**OBS:** Due the time it takes to full update the information, your web browser might show a timeout page (like HTTP Code 504) even though it actually worked. You can try to configure proxy_read_timeout on your netbox nginx, and timeout in gunicorn.

---

## 5. Enable Logs

So that Proxbox plugin logs what is happening to the terminal, copy the following code and paste to `configuration.py` Netbox configuration file:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

You can customize this using the following link: [Django Docs - Logging](https://docs.djangoproject.com/en/dev/topics/logging/).
Although the above standard configuration should do the trick to things work.

---

## 6. Contributing

This project is based on commits and pull requests from [netdevopsbr/netbox-proxbox](https://github.com/netdevopsbr/netbox-proxbox)

Developing tools for this project based on [ntc-netbox-plugin-onboarding](https://github.com/networktocode/ntc-netbox-plugin-onboarding) repo.

Issues and pull requests are welcomed.
