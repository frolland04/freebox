#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example clears the DHCP leases from the Freebox.
"""

import asyncio
import json
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

    # Dump DHCP static leases
    # -----------------------

    fbx_dhcp_static_leases = await fbx.dhcp.get_dhcp_static_leases()
    print("fbx_dhcp_static_leases", type(fbx_dhcp_static_leases))

    fbx_dhcp_leases_lst=list()

    if fbx_dhcp_static_leases != None and len(fbx_dhcp_static_leases) != 0:
        for index, elt in enumerate(fbx_dhcp_static_leases, start=1):
            print(index,
                "'" + elt["mac"]     + "'",
                "'" + elt["ip"]      + "'",
                "'" + elt["comment"] + "'")
            fbx_dhcp_leases_lst.append(elt["mac"])

        print(fbx_dhcp_leases_lst)

        for mac in fbx_dhcp_leases_lst:
            print("=> Deleting", mac)
            await fbx.dhcp.delete_dhcp_static_lease(mac)
    else:
        print("No static leases.")

    # Dump LAN hosts using lan API
    # ----------------------------
    fbx_lan_hosts = await fbx.lan.get_hosts_list()
    print("fbx_lan_hosts", type(fbx_lan_hosts))

    fbx_lan_hosts_lst=list()
    
    if fbx_lan_hosts != None and len(fbx_lan_hosts) != 0:
        for index, elt in enumerate(fbx_lan_hosts, start=1):
            print(index,
                "'" + elt["primary_name"]  + "'",
                "'" + elt["id"] + "'")
            fbx_lan_hosts_lst.append(elt["id"])

        print(fbx_lan_hosts_lst)

        for id in fbx_lan_hosts_lst:
            print("=> Deleting", id)
            try:
                await fbx.lan.delete_lan_host(id)
            except Exception as e:
                print("ERROR", e)
    else:
        print("No LAN host leases.")
        
    # Close the freebox session
    await fbx.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(demo())
loop.close()