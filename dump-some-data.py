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

    fbx_perms = await fbx.get_permissions()
    print("permissions", type(fbx_perms), fbx_perms)

    # Dump Freebox configuration using system API
    # -------------------------------------------
    fbx_system = await fbx.system.get_config()
    print("fbx_system", type(fbx_system))

    # Dump DHCP configuration using dhcp API
    # --------------------------------------
    fbx_dhcp = await fbx.dhcp.get_config()
    print("fbx_dhcp", type(fbx_dhcp))
    print("fbx_dhcp.enabled",        fbx_dhcp["enabled"])
    print("fbx_dhcp.gateway",        fbx_dhcp["gateway"])
    print("fbx_dhcp.ip_range_start", fbx_dhcp["ip_range_start"])
    print("fbx_dhcp.ip_range_end",   fbx_dhcp["ip_range_end"])
    print("fbx_dhcp.netmask",        fbx_dhcp["netmask"])
    print("fbx_dhcp.dns",            fbx_dhcp["dns"])

    fbx_dhcp_leases = await fbx.dhcp.get_dhcp_static_leases()
    print("fbx_dhcp_leases", type(fbx_dhcp_leases))
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
    for index, elt in enumerate(fbx_lan_hosts, start=1):
        print(index,
              "'" + elt["primary_name"]  + "'",
              "'" + elt["vendor_name"]   + "'",
              "'" + elt["l2ident"]["id"] + "'")

    # Get the phonecall log
    # ---------------------
    fbx_calls = await fbx.call.get_calls_log()
    print("fbx_calls", type(fbx_calls))
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
