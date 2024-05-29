#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example can be run safely as it only dumps some data from the Freebox.
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

    # Dump DHCP configuration using dhcp API
    # --------------------------------------
    fbx_dhcp = await fbx.dhcp.get_config()
    print("fbx_dhcp", type(fbx_dhcp))
    print("--")

    print("fbx_dhcp.enabled",        fbx_dhcp["enabled"])
    print("fbx_dhcp.gateway",        fbx_dhcp["gateway"])
    print("fbx_dhcp.ip_range_start", fbx_dhcp["ip_range_start"])
    print("fbx_dhcp.ip_range_end",   fbx_dhcp["ip_range_end"])
    print("fbx_dhcp.netmask",        fbx_dhcp["netmask"])
    print("fbx_dhcp.dns",            fbx_dhcp["dns"])
    print("--")

    # Alter and dump DHCP static leases
    # ---------------------------------

    # -- dummy_lease = {"ip": "192.168.1.2", "mac": "00:11:22:33:44:55", "comment": "test static DHCP lease"}
    # -- await fbx.dhcp.create_dhcp_static_lease(dummy_lease)
    # -- await fbx.dhcp.edit_dhcp_static_lease(dummy_lease["mac"], dummy_lease)

    fbx_dhcp_static_leases = await fbx.dhcp.get_dhcp_static_leases()
    print("fbx_dhcp_static_leases", type(fbx_dhcp_static_leases))
    print("--")

    fbx_dhcp_output_lst=list()

    for index, elt in enumerate(fbx_dhcp_static_leases, start=1):
        print(index,
              "'" + elt["mac"]     + "'",
              "'" + elt["ip"]      + "'",
              "'" + elt["comment"] + "'")
        fbx_dhcp_output_lst.append({"mac": elt["mac"], "ip": elt["ip"], "comment": elt["comment"]})

    # Dump LAN hosts using lan API
    # ----------------------------
    fbx_lan_hosts = await fbx.lan.get_hosts_list()
    print("fbx_lan_hosts", type(fbx_lan_hosts))
    print("--")

    for index, elt in enumerate(fbx_lan_hosts, start=1):
        print(index,
              "'" + elt["primary_name"]  + "'",
              "'" + elt["l2ident"]["id"] + "'")
        fbx_dhcp_output_lst.append({"mac": elt["l2ident"]["id"], "ip": "", "comment": elt["primary_name"]})

    # Save DHCP leases + LAN hosts to JSON
    with open("dhcp-leases.json", "w") as of:
        json.dump(fbx_dhcp_output_lst, of)

    # Close the freebox session
    await fbx.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(demo())
loop.close()