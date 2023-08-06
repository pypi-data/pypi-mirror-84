"""
Utilities for Folder Custodian Service.
"""

TEMPLATE = """
[Unit]
Description=Folder Custodian Service

[Service]
Type=oneshot
ExecStart=/bin/true
ExecStop=fcust run $COMMON_FOLDER_PATH

[Install]
WantedBy=multi-user.target
"""


# Add function to build template according to requested directory

# Add function to set up the user service properly
# https://wiki.archlinux.org/index.php/Systemd/User
# https://superuser.com/questions/1037466/how-to-start-a-systemd-service-after-user-login-and-stop-it-before-user-logout/1269158
# https://askubuntu.com/questions/293312/execute-a-script-upon-logout-reboot-shutdown-in-ubuntu/796157#796157

# Add function to start the service

# Add CLI commands for the last two functions
