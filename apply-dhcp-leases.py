#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example sets a custom DHCP configuration to the Freebox.
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

    fbx_dhcp_static_leases = await fbx.dhcp.get_dhcp_static_leases()
    print("fbx_dhcp_static_leases", type(fbx_dhcp_static_leases))
    print("--")

    if fbx_dhcp_static_leases != None:
        print("Could not set new DHCP leases if existing leases remain. Please clear them first.")
        print("Exiting!")
        exit(5)

    # Read DHCP leases
    fbx_dhcp_input_lst = list()
    with open("dhcp-leases.json", "r") as input_file:
        fbx_dhcp_input_lst = json.load(input_file)
    print("fbx_dhcp_input_lst", fbx_dhcp_input_lst)

    answer = input("Apply (DANGEROUS) ? [Y/N]")
    if answer.lower() in ["y","yes"]:
        # Doing the job
        print("Applying changes (dhcp)")
        try:
            for elt in fbx_dhcp_input_lst:
                print("=> Adding",
                      "'" + elt["mac"]     + "'",
                      "'" + elt["ip"]      + "'",
                      "'" + elt["comment"] + "'")
                await fbx.dhcp.create_dhcp_static_lease(elt)
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