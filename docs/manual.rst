=====================================
Zabbix-CLI
=====================================

|
| Rafael Martinez Guerrero (University of Oslo)
| E-mail: rafael@postgresql.org.es
|
| Source: https://github.com/unioslo/zabbix-cli
|

.. contents::


Introduction
============

Zabbix-cli is a terminal client for managing Zabbix
administration tasks via the Zabbix API.

The zabbix-cli code is distributed under the GNU General Public
License 3 and it is written in Python. It has been developed and
tested by members of the Department for IT Infrastructure at the
Center for Information Technology at the University of Oslo, Norway.


Main features
=============

* Terminal client
* Two execution modes available: Zabbix-CLI shell and commandline.
* 54 zabbix-CLI commands available.
* Multilevel configuration system.
* Possibility to define Bulk updates. Several performance improvements
  are used when running in bulk modus.
* Authentication-token, authentication-file and environment variables
  support for autologin.
* Support for plain, CSV and JSON output.
* Online help
* Written in Python.


Configuration
=============

Configuration file
------------------

Zabbix-cli has a **multilevel configuration system.**

This means that we do not override entire configuration files but we
merge all the defined configuration files in our system and use the
parameter values defined in the configuration file with higher
priority if a parameter is defined in more than one file.

The ordered list with the files with higher on top:

#. ``/usr/share/zabbix-cli/zabbix-cli.fixed.conf``
#. ``/etc/zabbix-cli/zabbix-cli.fixed.conf``
#. Configuration file defined with the parameter ``-c`` / ``--config`` when executing zabbix-cli
#. ``$HOME/.zabbix-cli/zabbix-cli.conf``
#. ``/etc/zabbix-cli/zabbix-cli.conf``
#. ``/usr/share/zabbix-cli/zabbix-cli.conf``

The default configuration file can be found in
``/usr/share/zabbix-cli/zabbix-cli.conf`` or ``etc/zabbix-cli.conf``
in the source code.

The easiest way to configurate your client will be running this
command to create your own ``$HOME/.zabbix-cli/zabbix-cli.conf``
file.::

  # zabbix-cli-init <zabbix API url>

The parameter ``zabbix_api_url`` must be defined in the configuration
file. Without this parameter, ``zabbix-cli`` will not know where to
connect. This parameter will be defined automatically if you have run
the command ``zabbix-cli-init``.

Remember to activate logging with ``logging=ON`` if you want to
activate logging. The user running ``zabbix-cli`` must have read/write
access to the log file defined with ``log_file``. This parameter will
be defined automatically with an OFF value if you have run the command
``zabbix-cli-init``.

To see all the active configuration files in your system and the
configuration parameters that zabbix-cli is using, use
``show_zabbixcli_config``::

  [zabbix-cli rafael@zabbix-ID]$ show_zabbixcli_config

  +----------------------------------------------+
  | Active configuration files                   |
  +----------------------------------------------+
  | */usr/share/zabbix-cli/zabbix-cli.fixed.conf |
  | */etc/zabbix-cli/zabbix-cli.fixed.conf       |
  | */root/.zabbix-cli/zabbix-cli.conf           |
  | */etc/zabbix-cli/zabbix-cli.conf             |
  | */usr/share/zabbix-cli/zabbix-cli.conf       |
  +----------------------------------------------+

  +--------------------------------------+---------------------------------------+
  |              Configuration parameter | Value                                 |
  +--------------------------------------+---------------------------------------+
  |                       zabbix_api_url | https://zabbix.example.org            |
  |                          cert_verify | ON                                    |
  |                            system_id | zabbix-ID                             |
  |                    default_hostgroup | All-hosts                             |
  |              default_admin_usergroup | Zabbix-admin                          |
  |        default_create_user_usergroup | All-users                             |
  | default_notification_users_usergroup | All-notification-users                |
  |            default_directory_exports | /home/user/zabbix_exports             |
  |                default_export_format | XML                                   |
  |    include_timestamp_export_filename | ON                                    |
  |                           use_colors | ON                                    |
  |                           use_paging | OFF                                   |
  |                  use_auth_token_file | ON                                    |
  |                              logging | ON                                    |
  |                            log_level | INFO                                  |
  |                             log_file | /home/user/.zabbix-cli/zabbix-cli.log |
  +--------------------------------------+---------------------------------------+


Environment Authentication
--------------------------

You can define the ``ZABBIX_USERNAME`` and ``ZABBIX_PASSWORD`` environment
variables to pass authentication credentials to ``zabbix-cli``.

For example:

::

   export ZABBIX_USERNAME=zbxuser
   read -srp "Zabbix Password: " ZABBIX_PASSWORD; export ZABBIX_PASSWORD;
   zabbix-cli

**NOTE**: It is important to remember that this method will save the password in clear text in a environment variable. This value will be available to other processes running in the same session.


Authentication file
-------------------

You can define the file ``$HOME/.zabbix-cli_auth`` if you want to
avoid to write your username and password everytime you use
``zabbix-cli``. This can be useful if you are running ``zabbix-cli``
in non-interactive modus from scripts or automated jobs.

The format of this file is a line with this information::

  USERNAME::PASSWORD

**NOTE:** The password will be saved in clear text so be careful with the information saved here and restrict access to this file only to your user. ``chmod 400 ~/.zabbix-cli_auth`` will be defined by ``zabbix-cli`` on this file the first time it uses it.


Authentication token file
-------------------------

The file ``$HOME/.zabbix-cli_auth_token`` will be created with
information about the API-auth-token from the last login if the
parameter ``use_auth_token_file=ON`` is defined in the configuration
file.

The information in this file will be used, if we can, to avoid having to
write the username and password everytime you use ``zabbix-cli``. This
can be useful if you are running ``zabbix-cli`` in non-interactive
modus from scripts or automated jobs.

This authentication method will work as long as the API-auth-token
saved is active in Zabbix. The ``Auto-logout`` attribute of the user
will define how long the API-auth-token will be active.

If the API-auth-token is not valid, ``zabbix-cli`` will delete the
file ``$HOME/.zabbix-cli_auth_token`` and you will have to login again
with a valid username and password.


Zabbix-CLI shell
================

The Zabbix-CLI interactive shell can be started by running the program
``/usr/bin/zabbix-cli``

::

   [user@host]# zabbix-cli

   #############################################################
   Welcome to the Zabbix command-line interface (v2.1.0)
   Connected to server https://zabbix.example.org (v4.0.6)
   #############################################################
   Type help or \? to list commands.

   [zabbix-cli user@zabbix-ID]$ help

   Documented commands (type help <topic>):
   ========================================
   EOF                             show_alarms
   acknowledge_event               show_global_macros
   acknowledge_trigger_last_event  show_history
   add_host_to_hostgroup           show_host
   add_user_to_usergroup           show_host_inventory
   add_usergroup_permissions       show_host_usermacros
   clear                           show_hostgroup
   create_host                     show_hostgroup_permissions
   create_host_interface           show_hostgroups
   create_hostgroup                show_hosts
   create_maintenance_definition   show_items
   create_notification_user        show_last_values
   create_user                     show_maintenance_definitions
   create_usergroup                show_maintenance_periods
   define_global_macro             show_template
   define_host_monitoring_status   show_templates
   define_host_usermacro           show_trigger_events
   export_configuration            show_triggers
   help                            show_usergroup
   import_configuration            show_usergroup_permissions
   link_template_to_host           show_usergroups
   load_balance_proxy_hosts        show_usermacro_host_list
   move_proxy_hosts                show_usermacro_template_list
   quit                            show_users
   remove_host                     show_zabbixcli_config
   remove_host_from_hostgroup      unlink_template_from_host
   remove_maintenance_definition   update_host_inventory
   remove_user                     update_host_proxy
   remove_user_from_usergroup      update_usergroup_permissions
   shell

   Miscellaneous help topics:
   ==========================
   shortcuts  support

**NOTE:** It is possible to use Zabbix-CLI in a non-interactive mode
by running ``/usr/bin/zabbix-cli`` with the parameter ``--command
<zabbix_command>`` or ``-C <zabbix_command>`` in the OS shell. This
can be used to run ``zabbix-cli`` commands from shell scripts or other
programs .e.g.

::

   [user@host]# zabbix-cli -C "show_usergroups"

   +---------+---------------------------+--------------------+-------------+
   | GroupID | Name                      |     GUI access     |    Status   |
   +---------+---------------------------+--------------------+-------------+
   |      13 | DBA                       | System default (0) |  Enable (0) |
   |       9 | Disabled                  | System default (0) | Disable (1) |
   |      11 | Enabled debug mode        | System default (0) |  Enable (0) |
   |       8 | Guests                    |    Disable (2)     | Disable (1) |
   |      12 | No access to the frontend |    Disable (2)     |  Enable (0) |
   |      49 | testgroup                 | System default (0) |  Enable (0) |
   |      15 | Test users                | System default (0) |  Enable (0) |
   |      16 | Test users intern         |    Internal (1)    |  Enable (0) |
   |       7 | Zabbix administrators     |    Internal (1)    |  Enable (0) |
   |      14 | Zabbix core               | System default (0) |  Enable (0) |
   +---------+---------------------------+--------------------+-------------+

It is possible to use the parameter ``--file <zabbix_command_file>`` or
``-f <zabbix_command_file>`` to define a file with multiple ``zabbix-cli``
commands for scripting.

Some performance improvements get activated when executing
``zabbix-cli`` in this way. The perfomance gain when running multiple
commands via an input file can be as high as 70% when creating new
hosts in Zabbix.

::

   [user@host]# cat zabbix_input_file.txt

   # This a comment.
   # Creating hosts.

   create_host test000001.example.net All-manual-hosts .+ 1
   create_host test000002.example.net All-manual-hosts .+ 1
   create_host test000003.example.net All-manual-hosts .+ 1

   # Deleting hosts

   remove_host test000001.example.net
   remove_host test000002.example.net
   remove_host test000003.example.net

   [user@host]# zabbix-cli -f zabbix_input_file.txt

   [OK] File [/home/user/zabbix_input_file.txt] exists. Bulk execution of commands defined in this file started.

   [Done]: Host (test000001.example.net) with ID: 14213 created
   [Done]: Host (test000002.example.net) with ID: 14214 created
   [Done]: Host (test000003.example.net) with ID: 14215 created
   [Done]: Hosts (test000001.example.net) with IDs: 14213 removed
   [Done]: Hosts (test000002.example.net) with IDs: 14214 removed
   [Done]: Hosts (test000003.example.net) with IDs: 14215 removed


One can also use the parameters ``--output csv`` or
``--output json`` when running ``zabbix-cli`` in non-interactive
modus to generate an output in CSV or JSON format.

::

   [user@host ~]# zabbix-cli --output csv show_usergroups

   "13","DBA","System default (0)","Enable (0)"
   "9","Disabled","System default (0)","Disable (1)"
   "11","Enabled debug mode","System default (0)","Enable (0)"
   "8","Guests","Disable (2)","Disable (1)"
   "12","No access to the frontend","Disable (2)","Enable (0)"
   "49","testgroup","System default (0)","Enable (0)"
   "15","Test users","System default (0)","Enable (0)"
   "16","Test users intern","Internal (1)","Enable (0)"
   "7","Zabbix administrators","Internal (1)","Enable (0)"
   "14","Zabbix core","System default (0)","Enable (0)"


Remember that you have to use ``""`` and escape some characters if
running commands in non-interactive mode with parameters that have spaces
or special characters for the shell, .e.g.

::

   [user@host ~]# zabbix-cli -C "show_host * \"'available':'2','maintenance_status':'1'\" "

   +--------+----------------------+-------------------------+-----------------------------------+--------------------+-----------------+-----------------+---------------+
   | HostID | Name                 | Hostgroups              | Templates                         | Applications       |   Zabbix agent  |   Maintenance   |     Status    |
   +--------+----------------------+-------------------------+-----------------------------------+--------------------+-----------------+-----------------+---------------+
   |  10110 | test01.uio.no        | [8] Database servers    | [10102] Template App SSH Service  | CPU                | Unavailable (2) | In progress (1) | Monitored (0) |
   |        |                      |                         | [10104] Template ICMP Ping        | Filesystems        |                 |                 |               |
   |        |                      |                         | [10001] Template OS Linux         | General            |                 |                 |               |
   |        |                      |                         |                                   | ICMP               |                 |                 |               |
   |        |                      |                         |                                   | Memory             |                 |                 |               |
   |        |                      |                         |                                   | Network interfaces |                 |                 |               |
   |        |                      |                         |                                   | OS                 |                 |                 |               |
   |        |                      |                         |                                   | Performance        |                 |                 |               |
   |        |                      |                         |                                   | Processes          |                 |                 |               |
   |        |                      |                         |                                   | SSH service        |                 |                 |               |
   |        |                      |                         |                                   | Security           |                 |                 |               |
   |        |                      |                         |                                   | Zabbix agent       |                 |                 |               |
   +--------+----------------------+-------------------------+-----------------------------------+--------------------+-----------------+-----------------+---------------+
   |  10484 | test02.uio.no        | [12] Web servers        | [10094] Template App HTTP Service | HTTP service       | Unavailable (2) | In progress (1) | Monitored (0) |
   |        |                      | [13] PostgreSQL servers | [10073] Template App MySQL        | ICMP               |                 |                 |               |
   |        |                      | [17] MySQL servers      | [10102] Template App SSH Service  | MySQL              |                 |                 |               |
   |        |                      | [21] ssh servers        | [10104] Template ICMP Ping        | SSH service        |                 |                 |               |
   |        |                      | [5] Discovered hosts    |                                   |                    |                 |                 |               |
   |        |                      | [8] Database servers    |                                   |                    |                 |                 |               |
   +--------+----------------------+-------------------------+-----------------------------------+--------------------+-----------------+-----------------+---------------+
   |  10427 | test03.uio.no        | [12] Web servers        | [10094] Template App HTTP Service | HTTP service       | Unavailable (2) | In progress (1) | Monitored (0) |
   |        |                      | [17] MySQL servers      | [10073] Template App MySQL        | ICMP               |                 |                 |               |
   |        |                      | [21] ssh servers        | [10102] Template App SSH Service  | MySQL              |                 |                 |               |
   |        |                      | [5] Discovered hosts    | [10104] Template ICMP Ping        | SSH service        |                 |                 |               |
   |        |                      | [8] Database servers    |                                   |                    |                 |                 |               |
   +--------+----------------------+-------------------------+-----------------------------------+--------------------+-----------------+-----------------+---------------+


Interactive shell commands
==========================

.. autoclass:: zabbix_cli.cli::zabbixcli
   :members:

Authors
=======

In alphabetical order:

|
| Rafael Martinez Guerrero
| E-mail: rafael@postgresql.org.es / rafael@usit.uio.no
| PostgreSQL-es / University Center for Information Technology (USIT), University of Oslo, Norway
|

License and Contributions
=========================

Zabbix-CLI is the property of USIT-University of Oslo, and its code is
distributed under GNU General Public License 3.

| Copyright © 2014-2017 USIT-University of Oslo.
