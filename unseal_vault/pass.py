

def get_config_passtore(pass_name):
    '''
    Get config in passwordstore and convert it as yaml

    *pass_name* is the name of documents contain config
    '''
    stream = run_cmd('pass show {}'.format(pass_name))
    try:
        return yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(1)
