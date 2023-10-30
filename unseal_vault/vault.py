import hvac


def unseal(scheme, host, port, unseal_keys, name=None):
    """
    Unseal one server

    *host* the hostname or ip server want to unlock

    *port* the Vault TCP port

    *unseal_keys* the unseal keys list
    """
    url = f"{scheme}://{host}:{port}"
    print(f"Connect to URL: {url}")

    if name:
        print(f"{name}:")
    client = hvac.Client(url=url, verify=False)
    if client.sys.is_sealed():
        print("Server sealed")
        client.sys.submit_unseal_keys(unseal_keys)
        if client.sys.is_sealed():
            print("Server still sealed")
        else:
            print("Server unsealed")
    else:
        print("Server unsealed")
