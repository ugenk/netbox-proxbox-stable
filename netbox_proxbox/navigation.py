from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

fullupdate_item = PluginMenuItem(
    link='plugins:netbox_proxbox:home',
    link_text='Full Update',
)

contributing_item = PluginMenuItem(
    link='plugins:netbox_proxbox:contributing',
    link_text='Contributing!',
)

community_item = PluginMenuItem(
    link='plugins:netbox_proxbox:community',
    link_text='Community',
    buttons=[
        PluginMenuButton(
            "plugins:netbox_proxbox:discussions",
            "GitHub Discussions",
            "mdi mdi-github",
        ),
        PluginMenuButton(
            "plugins:netbox_proxbox:discord",
            "Discord Community",
            "mdi mdi-forum",
        ),
        PluginMenuButton(
            "plugins:netbox_proxbox:telegram",
            "Telegram Community",
            "mdi mdi-send",
        ),
    ]
)

menu = PluginMenu(
    label='Proxbox',
    groups=(
        ('Proxmox Plugin', (fullupdate_item,)),
        ('Join our community', (contributing_item, community_item,)),
    ),
    icon_class='mdi mdi-dns'
)