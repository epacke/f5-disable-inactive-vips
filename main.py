import requests, os
from f5 import F5rest, logger
from datetime import datetime

loadbalancers = ['bigip-01.domain.com']

for lb in loadbalancers:
    client = F5rest('user', 'password', lb, verify_ssl=False)

    response = client.get_virtual_server_stats()
    no_connection_vips = [
        vs['nestedStats']['entries'] for vs in response['entries'].values()
        if vs['nestedStats']['entries']['clientside.totConns']['value'] == 0
    ]

    for vip in no_connection_vips:
        logger.info(f'Disabling {vip["tmName"]["description"]} on {lb}')
        client.disable_virtual_server(vip['tmName']['description'].replace('/', '~'),
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Auto disabled due to low connections'
        )