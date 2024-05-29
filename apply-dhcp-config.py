#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example sets a custom DHCP configuration to the Freebox.
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

    fbx_lan = await fbx.lan.get_config()
    print("fbx_lan", type(fbx_lan), fbx_lan)
    print("--")

    # Dump DHCP configuration using dhcp v4/v6 API
    # --------------------------------------------
    fbx_dhcp = await fbx.dhcp.get_config()
    print("fbx_dhcp", type(fbx_dhcp), fbx_dhcp)
    print("--")

    fbx_dhcp6 = await fbx.dhcp.get_v6_config()
    print("fbx_dhcp6", type(fbx_dhcp6), fbx_dhcp6)
    print("--")

    # Before changes
    print("+--- CURRENT CONFIGURATION --------------------------------------+")
    print("fbx_lan.mode",              fbx_lan["mode"])
    print("fbx_lan.ip",                fbx_lan["ip"])
    print("fbx_lan.name",              fbx_lan["name"])
    print("fbx_lan.name_dns",          fbx_lan["name_dns"])
    print("fbx_lan.name_mdns",         fbx_lan["name_mdns"])
    print("fbx_lan.name_netbios",      fbx_lan["name_netbios"])
    print("--")
    print("fbx_dhcp.enabled",          fbx_dhcp["enabled"])
    print("fbx_dhcp.gateway",          fbx_dhcp["gateway"])
    print("fbx_dhcp.ip_range_start",   fbx_dhcp["ip_range_start"])
    print("fbx_dhcp.ip_range_end",     fbx_dhcp["ip_range_end"])
    print("fbx_dhcp.netmask",          fbx_dhcp["netmask"])
    print("fbx_dhcp.dns",              fbx_dhcp["dns"])
    print("fbx_dhcp.always_broadcast", fbx_dhcp["always_broadcast"])
    print("fbx_dhcp.sticky_assign",    fbx_dhcp["sticky_assign"])
    print("+--- CURRENT CONFIGURATION --------------------------------------+")
    print("")

    # New configuration attributes
    fbx_lan["mode"]              = "router"
    fbx_lan["ip"]                = "192.168.0.254"
    fbx_lan["name"]              = "Freebox Server"
    fbx_lan["name_dns"]          = "freebox-server"
    fbx_lan["name_mdns"]         = "Freebox-Server"
    fbx_lan["name_netbios"]      = "Freebox-Server"
    fbx_dhcp["enabled"]          = True
    fbx_dhcp["gateway"]          = "192.168.0.254"
    fbx_dhcp["ip_range_start"]   = "192.168.0.1"
    fbx_dhcp["ip_range_end"]     = "192.168.0.199"
    fbx_dhcp["netmask"]          = "255.255.255.0"
    fbx_dhcp["dns"]              = ['192.168.0.254','8.8.8.8','8.8.4.4','']
    fbx_dhcp["always_broadcast"] = False
    fbx_dhcp["sticky_assign"]    = True

    # After changes
    print("+--- NEW CONFIGURATION ------------------------------------------+")
    print("fbx_lan.mode",              fbx_lan["mode"])
    print("fbx_lan.ip",                fbx_lan["ip"])
    print("fbx_lan.name",              fbx_lan["name"])
    print("fbx_lan.name_dns",          fbx_lan["name_dns"])
    print("fbx_lan.name_mdns",         fbx_lan["name_mdns"])
    print("fbx_lan.name_netbios",      fbx_lan["name_netbios"])
    print("--")
    print("fbx_dhcp.enabled",          fbx_dhcp["enabled"])
    print("fbx_dhcp.gateway",          fbx_dhcp["gateway"])
    print("fbx_dhcp.ip_range_start",   fbx_dhcp["ip_range_start"])
    print("fbx_dhcp.ip_range_end",     fbx_dhcp["ip_range_end"])
    print("fbx_dhcp.netmask",          fbx_dhcp["netmask"])
    print("fbx_dhcp.dns",              fbx_dhcp["dns"])
    print("fbx_dhcp.always_broadcast", fbx_dhcp["always_broadcast"])
    print("fbx_dhcp.sticky_assign",    fbx_dhcp["sticky_assign"])
    print("+--- NEW CONFIGURATION ------------------------------------------+")
    print("")

    answer = input("Apply (DANGEROUS) ? [Y/N]")
    if answer.lower() in ["y","yes"]:
        # Doing the job
        print("Applying changes (lan)")
        try:
            await fbx.lan.set_config(fbx_lan)
        except Exception as e:
            print("ERROR", e)

        print("Applying changes (dhcp)")
        try:
            await fbx.dhcp.set_config(fbx_dhcp)
        except Exception as e:
            print("ERROR", e)

        answer = input("Reboot ? [Y/N]")
        if answer.lower() in ["y","yes"]:
            # Reboot your Freebox !
            print("Rebooting")
            await fbx.system.reboot()
        else:
            print("No reboot.")
    else:
        # Ignore changes to Freebox
        print("Cancelled.")
        
    # Close the freebox session
    await fbx.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(demo())
loop.close()