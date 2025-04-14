ethereum_package_shared_utils = import_module(
    "github.com/ethpandaops/ethereum-package/src/shared_utils/shared_utils.star"
)

ethereum_package_cl_context = import_module(
    "github.com/ethpandaops/ethereum-package/src/cl/cl_context.star"
)

ethereum_package_constants = import_module(
    "github.com/ethpandaops/ethereum-package/src/package_io/constants.star"
)

constants = import_module("../../package_io/constants.star")
util = import_module("../../util.star")

# A null node is a node that does not perform any consensus.
# It's intended to be used alongside a execution layer with a built-in consensus client.

# Ports
BEACON_DISCOVERY_PORT_NUM = 9003
BEACON_HTTP_PORT_NUM = 8547

USED_PORTS = {
    constants.TCP_DISCOVERY_PORT_ID: PortSpec(
        number=BEACON_DISCOVERY_PORT_NUM, transport_protocol="TCP"
    ),
    constants.UDP_DISCOVERY_PORT_ID: PortSpec(
        number=BEACON_DISCOVERY_PORT_NUM, transport_protocol="UDP"
    ),
    constants.HTTP_PORT_ID: PortSpec(
        number=BEACON_HTTP_PORT_NUM,
        transport_protocol="TCP",
        application_protocol="HTTP",
    ),
}


def launch(
    plan,
    launcher,
    service_name,
    participant,
    __global_log_level, # ignored
    __persistent, # ignored
    tolerations,
    node_selectors,
    el_context,
    __existing_cl_clients, # ignored
    __l1_config_env_vars, # ignored
    __sequencer_enabled, # ignored
    __servability_helper, # ignored
    __interop_params, # ignored
    __da_server_context, # ignored
):
    cmd = ["dotnet", "Nethermind.Consensus.NullClient.dll"]

    # configure files
    files = {
        ethereum_package_constants.GENESIS_DATA_MOUNTPOINT_ON_CLIENTS: launcher.deployment_output,
        ethereum_package_constants.JWT_MOUNTPOINT_ON_CLIENTS: launcher.jwt_file,
    }

    # configure environment variables
    env_vars = dict(participant.cl_extra_env_vars)

    config_args = {
        "image": participant.cl_image,
        "ports": USED_PORTS,
        "cmd": cmd,
        "files": files,
        "private_ip_address_placeholder": ethereum_package_constants.PRIVATE_IP_ADDRESS_PLACEHOLDER,
        "env_vars": env_vars,
        "labels": ethereum_package_shared_utils.label_maker(
            client="null-node",
            client_type="beacon",
            image=util.label_from_image(participant.cl_image),
            connected_client=el_context.client_name,
            extra_labels=participant.cl_extra_labels,
        ),
        "tolerations": tolerations,
        "node_selectors": node_selectors,
    }

    # configure resources

    if participant.cl_min_cpu > 0:
        config_args["min_cpu"] = participant.cl_min_cpu
    if participant.cl_max_cpu > 0:
        config_args["max_cpu"] = participant.cl_max_cpu
    if participant.cl_min_mem > 0:
        config_args["min_memory"] = participant.cl_min_mem
    if participant.cl_max_mem > 0:
        config_args["max_memory"] = participant.cl_max_mem

    config = ServiceConfig(**config_args)

    service = plan.add_service(service_name, config)
    service_url = util.make_service_http_url(service)

    return ethereum_package_cl_context.new_cl_context(
        client_name=constants.CL_TYPE.null_node,
        enr="",
        ip_addr=service.ip_address,
        http_port=util.get_service_http_port_num(service),
        beacon_http_url=service_url,
        cl_nodes_metrics_info=[],
        beacon_service_name=service_name,
    )


def new_null_node_launcher(deployment_output, jwt_file, network_params):
    return struct(
        deployment_output=deployment_output,
        jwt_file=jwt_file,
        network_params=network_params,
    )
