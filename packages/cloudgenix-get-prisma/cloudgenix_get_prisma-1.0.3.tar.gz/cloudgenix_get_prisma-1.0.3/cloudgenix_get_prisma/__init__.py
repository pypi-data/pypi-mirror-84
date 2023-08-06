import os
import sys
import csv
import re
import argparse
from . gpcloudservice import GPCloudServiceOperations

SCRIPT_NAME = "Get Prisma Servicelinks"

try:
    import cloudgenix
except ImportError:
    print("ERROR: CloudGenix Python SDK required (try 'pip install cloudgenix')")
    sys.exit(1)

try:
    import cloudgenix_idname
except ImportError:
    print("ERROR: CloudGenix IDName module required (try 'pip install cloudgenix_idname')")
    sys.exit(1)

try:
    from tabulate import tabulate
except ImportError:
    print("ERROR: Tabulate Python module required (try 'pip install tabulate')")
    sys.exit(1)

# Try getting AUTH_TOKEN
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

# Try getting Prisma API key from env var
PRISMA_API_KEY = os.environ.get("PRISMA_API_KEY")

# regex
remotenet_re = re.compile(r'Prisma Access info on Panorama:\n {2}Remote Onboarding: (.*)\n {2}IPSEC')


def servicelinks(sdk=None, idname_obj=None, controller="https://api.elcapitan.cloudgenix.com", ssl_verify=True,
                 prisma_all_endpoints=False):

    prisma_name2ip = {}
    prisma_status = False

    if sdk is None:
        # need to instantiate
        sdk = cloudgenix.API(controller=controller, ssl_verify=ssl_verify)

    if not sdk.tenant_id:
        # need to login.
        if AUTH_TOKEN is None:
            sdk.interactive.login()
        else:
            sdk.interactive.use_token(AUTH_TOKEN)

    # Check Prisma API key if specified
    if PRISMA_API_KEY is not None:
        gpcs = GPCloudServiceOperations(PRISMA_API_KEY)
        print("Checking Prisma API Key.. ", end="", flush=True)
        prisma_status, prisma_name2ip, _, message = gpcs.remote_gw_addr_dicts()
        if not prisma_status:
            print("ERROR, message: {0}.".format(message), flush=True)
            sys.exit(1)
        else:
            print("Success." if message is None else "{0}.".format(message), flush=True)

    if sdk.tenant_id is None:
        print("ERROR: CloudGenix API Login failed, please check credentials or AUTH_TOKEN.")
        sys.exit(1)
    else:
        print("Logged into CloudGenix Tenant {0}.".format(sdk.tenant_name), flush=True)

    # gen id_name maps
    if idname_obj is None:
        id2n_obj = cloudgenix_idname.CloudGenixIDName(sdk)
    else:
        id2n_obj = idname_obj

    id2n_obj.update_sites_cache()
    id2n = id2n_obj.generate_sites_map()

    id2n_obj.update_elements_cache()
    id2n.update(id2n_obj.generate_elements_map())
    element_id2site = id2n_obj.generate_elements_map(key_val='id', value_val='site_id')
    element_id2connected = id2n_obj.generate_elements_map(key_val='id', value_val='connected')
    # cloudgenix.jd(element_id2connected)
    id2n_obj.update_interfaces_cache()
    id2n.update(id2n_obj.generate_interfaces_map())

    prisma_servicelinks = []
    for interface in id2n_obj.interfaces_cache:
        tags = interface.get('tags', [])
        if isinstance(tags, list) and 'AUTO-PRISMA_MANAGED' in tags:
            prisma_servicelinks.append(interface)

    servicelink_status_list = []

    for sl in prisma_servicelinks:
        description = sl.get('description', '')
        prisma_rno_list = remotenet_re.findall(description if description is not None else "")
        if len(prisma_rno_list) >= 1:
            prisma_rno = ";".join(prisma_rno_list)
        else:
            prisma_rno = "Unknown"

        element_id = sl.get('element_id')
        site_id = element_id2site.get(element_id, "Could not get site")
        element_connected = element_id2connected.get(element_id, False)
        interface_id = sl.get('id')
        parent_if_id = sl.get('parent')
        admin_state = sl.get('admin_up')

        # check for endpoint ip config
        sl_config = sl.get('service_link_config', {})
        if sl_config is not None:
            peer_config = sl_config.get('peer', {})
        else:
            peer_config = {}

        if peer_config is not None:
            conf_ip_list = peer_config.get('ip_addresses', [])
        else:
            conf_ip_list = []

        if len(conf_ip_list) == 0:
            conf_ip = "No IP"
        else:
            conf_ip = ";".join(conf_ip_list)

        resp = sdk.get.interfaces_status(site_id, element_id, interface_id)
        if not element_connected:
            # if element is not connected, status is stale.
            operational_state = "Unknown_Offline"
            extended_state = "Unknown_Offline"
        elif resp.cgx_status:
            operational_state = resp.cgx_content.get("operational_state")
            extended_state = resp.cgx_content.get("extended_state")
        else:
            operational_state = "Unknown"
            extended_state = "Unknown"

        site_name = id2n.get(site_id, site_id)
        element_name = id2n.get(element_id, element_id)
        interface_name = id2n.get(interface_id, interface_id)
        parent_if_name = id2n.get(parent_if_id, parent_if_id)

        if not prisma_status:
            servicelink_status_list.append({
                "Site": site_name,
                "Element": element_name,
                "Interface": interface_name,
                "Element Online": "Online" if element_connected else "Offline",
                "Admin State": str(admin_state),
                "Operational State": operational_state,
                "Extended State": extended_state,
                "Prisma Remote On-boarding": prisma_rno,
                "Parent Interface": parent_if_name,
                "Configured Endpoint": conf_ip
            })
        else:
            # in prisma endpoint IP mode. check if we want all tunnels or just admin down ones.
            if prisma_all_endpoints or admin_state is False:
                servicelink_status_list.append({
                    "Site": site_name,
                    "Element": element_name,
                    "Interface": interface_name,
                    "Element Online": "Online" if element_connected else "Offline",
                    "Admin State": str(admin_state),
                    "Operational State": operational_state,
                    "Extended State": extended_state,
                    "Prisma Remote On-boarding": prisma_rno,
                    "Parent Interface": parent_if_name,
                    "Configured Endpoint": conf_ip,
                    "Prisma API Endpoint IP": prisma_name2ip.get(prisma_rno)
                })

    return servicelink_status_list


def go():
    global PRISMA_API_KEY
    ############################################################################
    # Begin Script, start login / argument handling.
    ############################################################################

    # Parse arguments
    parser = argparse.ArgumentParser(description="{0}.".format(SCRIPT_NAME))

    # Allow Controller modification and debug level sets.
    controller_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    controller_group.add_argument("--controller", "-C",
                                  help="Controller URI, ex. https://api.elcapitan.cloudgenix.com",
                                  default="https://api.elcapitan.cloudgenix.com")

    controller_group.add_argument("--insecure", "-I", help="Disable SSL certificate and hostname verification",
                                  dest='verify', action='store_false', default=True)

    output_group = parser.add_argument_group('Output', 'These options change how the output is generated.')
    output_group.add_argument("--csv-output-file", help="Output as CSV to this specified file name",
                              type=str, default=None)

    pris_group = parser.add_argument_group('Prisma API', 'These options enable prisma API endpoint')
    pris_group.add_argument("--prisma-api-key", help="Activate Prisma Endpoint IP mode, giving Prisma API key "
                                                     "(or ENV var PRISMA_API_KEY)",
                            type=str, default=None)
    pris_group.add_argument("--all-endpoints", help="Return all endpoints in Prisma Endpoint IP mode",
                            action='store_true', default=False)

    args = vars(parser.parse_args())

    # set prisma API key if set from args
    local_prisma_api_key = args['prisma_api_key']
    if local_prisma_api_key:
        PRISMA_API_KEY = local_prisma_api_key

    servicelink_statuses = servicelinks(controller=args['controller'], ssl_verify=args['verify'],
                                        prisma_all_endpoints=args['all_endpoints'])

    if len(servicelink_statuses) == 0:
        print("No Prisma CloudBlade links found. Exiting.")
        sys.exit(0)

    header = servicelink_statuses[0].keys()
    rows = [servicelink.values() for servicelink in servicelink_statuses]

    if args['csv_output_file'] is None:
        print(tabulate(rows, header))
    else:
        # write CSV

        with open(args['csv_output_file'], 'wt') as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(header)  # write header
            csv_writer.writerows(rows)
    return


if __name__ == "__main__":
    # Get prisma
    go()

