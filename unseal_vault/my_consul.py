import consul


def consul_get_vault_server(
    vault_name, consul_host="127.0.0.1", consul_port="8500", consul_scheme="http"
):
    """
    Get vault server list in Consul
    And keep only important fields

    *vault_name* is the Vault service name defined in Consul
    """
    consul_client = consul.Consul(
        host=consul_host, port=consul_port, scheme=consul_scheme, verify=False
    )

    servers = list(
        map(
            lambda e: {
                "node_name": e["Node"],
                "address": e["ServiceAddress"],
                "port": e["ServicePort"],
            },
            consul_client.catalog.service(vault_name)[1],
        )
    )
    return servers
