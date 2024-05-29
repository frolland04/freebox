#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example can be run safely as it only dumps some data from the Freebox.
"""

import asyncio
from freebox_api import Freepybox


async def demo():
    # Instantiate Freepybox class
    fbx = Freepybox()

    # NOTE : To find out the 'https' hostname and port number of your Freebox, go to
    # *** http://mafreebox.freebox.fr/api_version ***

    # Connect to the Freebox
    # ----------------------
    # Be ready to authorize the application on the Freebox.
    await fbx.open(host="mafreebox.freebox.fr", port=80)

    print("fbx", type(fbx))
    print("api_version", fbx.api_version)
    print("--")

    fbx_perms = await fbx.get_permissions()
    print("permissions", type(fbx_perms), fbx_perms)
    print("--")

    # Dump Freebox configuration using system/lan API
    # -----------------------------------------------
    fbx_system = await fbx.system.get_config()
    print("fbx_system", type(fbx_system), fbx_system)
    print("--")

    print("fbx_system.mac",               fbx_system["mac"])
    print("fbx_system.box_flavor",        fbx_system["box_flavor"])
    print("fbx_system.board_name",        fbx_system["board_name"])
    print("fbx_system.box_authenticated", fbx_system["box_authenticated"])
    print("fbx_system.serial",            fbx_system["serial"])
    print("fbx_system.firmware_version",  fbx_system["firmware_version"])
    print("fbx_system.temp_cpub",         fbx_system["temp_cpub"])
    print("fbx_system.temp_cpum",         fbx_system["temp_cpum"])
    print("fbx_system.temp_hdd",          fbx_system["temp_hdd"])
    print("fbx_system.temp_sw",           fbx_system["temp_sw"])
    print("fbx_system.fan_rpm",           fbx_system["fan_rpm"])
    print("fbx_system.uptime",            fbx_system["uptime"])
    print("fbx_system.uptime_val",        fbx_system["uptime_val"])
    print("fbx_system.disk_status",       fbx_system["disk_status"])

    fbx_lan = await fbx.lan.get_config()
    print("fbx_lan", type(fbx_lan), fbx_lan)
    print("--")

    print("fbx_lan.mode",         fbx_lan["mode"])
    print("fbx_lan.ip",           fbx_lan["ip"])
    print("fbx_lan.name",         fbx_lan["name"])
    print("fbx_lan.name_dns",     fbx_lan["name_dns"])
    print("fbx_lan.name_mdns",    fbx_lan["name_mdns"])
    print("fbx_lan.name_netbios", fbx_lan["name_netbios"])
    print("--")

    # Dump DHCP configuration using dhcp API
    # --------------------------------------
    fbx_dhcp = await fbx.dhcp.get_config()
    print("fbx_dhcp", type(fbx_dhcp))
    print("--")

    print("fbx_dhcp.enabled",          fbx_dhcp["enabled"])
    print("fbx_dhcp.gateway",          fbx_dhcp["gateway"])
    print("fbx_dhcp.ip_range_start",   fbx_dhcp["ip_range_start"])
    print("fbx_dhcp.ip_range_end",     fbx_dhcp["ip_range_end"])
    print("fbx_dhcp.netmask",          fbx_dhcp["netmask"])
    print("fbx_dhcp.dns",              fbx_dhcp["dns"])
    print("fbx_dhcp.always_broadcast", fbx_dhcp["always_broadcast"])
    print("fbx_dhcp.sticky_assign",    fbx_dhcp["sticky_assign"])
    print("--")

    fbx_dhcp_leases = await fbx.dhcp.get_dhcp_static_leases()
    print("fbx_dhcp_leases", type(fbx_dhcp_leases))
    print("--")

    if fbx_dhcp_leases != None and len(fbx_dhcp_leases) != 0:
        for index, elt in enumerate(fbx_dhcp_leases, start=1):
            print(index,
                "'" + elt["mac"]     + "'",
                "'" + elt["ip"]      + "'",
                "'" + elt["hostname"]+ "'",
                "'" + elt["comment"] + "'")

    # Dump LAN hosts using lan API
    # ----------------------------
    fbx_lan_hosts = await fbx.lan.get_hosts_list()
    print("fbx_lan_hosts", type(fbx_lan_hosts))
    print("--")

    if fbx_lan_hosts != None and len(fbx_lan_hosts) != 0:
        for index, elt in enumerate(fbx_lan_hosts, start=1):
            print(index,
                "'" + elt["primary_name"]  + "'",
                "'" + elt["vendor_name"]   + "'",
                "'" + elt["l2ident"]["id"] + "'")

    # Get the phonecall log
    # ---------------------
    fbx_calls = await fbx.call.get_calls_log()
    print("fbx_calls", type(fbx_calls))
    print("--")

    for elt in fbx_calls:
        print(elt)

    # Reboot your Freebox !
    # ---------------------
    # -- await fbx.system.reboot()

    # Close the freebox session
    await fbx.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(demo())
loop.close()
