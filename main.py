import datetime
import os
import fake_useragent
from requests import Session
import re
import urllib3
import time
import art

urllib3.disable_warnings()


def write_check_results_to_file(results:list, w_file='check_results') -> None:
    """Function to write results to output file for farther usage"""
    w_file += datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')+'.csv'
    if not os.path.isfile(w_file):
        with open(w_file, 'a') as fw:
            fw.write(f'proxy; status code; availability; duration of request in seconds; current date; host \n')
    with open(w_file, 'a') as fw:
        [fw.write(f'{results[0][i]};'
                  f'{results[1][i][0]};'
                  f'{results[1][i][1]};'
                  f'{results[1][i][2]};'
                  f'{results[1][i][3].strftime("%Y.%m.%d %H-%M-%S")};'
                  f'{results[1][i][4]}'
                  f' \n')
            for i in range(0, len(results[0]))]

def load_proxies(p_file='proxies.txt') -> list:
    """
    Function to read proxies from file. It is possible to comment proxy in file.
    So it will look like as following:
    \n
    socks5://72.221.164.34:60671 # USA \n
    #socks5://188.133.137.133:14211 # Russian Federation \n
    #socks5://212.152.35.114:1080 \n
    \n
    The first string has comment after proxy delimited by; # \n
    The second string commented by # placed at the first position (will not be given to list of proxies); \n
    The third string also commented and will not be given to list of proxies.

    :param p_file: txt file which store proxies.
    :return: list includes not commented proxies
    """
    if os.path.isfile(p_file):
        with open(p_file, 'r') as f_proxies:
            proxies = f_proxies.read().split('\n')
    else:
        proxies = list()
    proxies = [item.split('#')[0].strip()
               for item in proxies
               if not (re.match('^#', item))]
    return proxies


def test_single_proxy(proc_host: str, proxy: str) -> tuple:
    """
    Function to make test request with proxy
    :param proc_host:
    :param proxy:
    :return: represented by tuple (status_code, status_check, duration_of_request)
    """
    app_header = {'user-agent': fake_useragent.UserAgent().random}
    session = Session()

    if re.match('http://', proc_host):
        session.proxies['http'] = proxy
    elif re.match('https://', proc_host):
        session.proxies['https'] = proxy
    elif re.match('socks4://', proc_host):
        session.proxies['socks4'] = proxy
    elif re.match('socks5://', proc_host):
        session.proxies['socks5'] = proxy
    else:
        session.proxies['socks5'] = proxy

    proxy_status = False
    status_code = None
    diff_time = None

    try:
        start_time = time.time()
        response = session.get(proc_host, headers=app_header, verify=False)
        diff_time = (time.time()-start_time).__round__(2)
        status_code = response.status_code
        if response.status_code == 200:
            proxy_status = True
        else:
            print(f'Bad proxy (inappropriate statuscode): {session.proxies}')
    except Exception as exception_err:
        print(exception_err)
        print(f'Bad proxy: {session.proxies}')

    print('~~~ Processing of proxy: ~~{}~~ finished at ~~{}~~ with code ~~~{}~~~ with time delay ~~~{}~~~'.format(proxy,
                                                  datetime.datetime.now().strftime('%Y.%m.%d %H-%M-%S'),
                                                  status_code,
                                                  diff_time))
    return status_code, proxy_status, diff_time, datetime.datetime.now(), host


def group_proxies_testing(proc_proxies_list: list, proc_host: str) -> list:
    """
    Function to group testing proxies
    :param proc_proxies_list: list of proxies, for example [socks5://72.221.164.34:60671,]
    :param proc_host: host to check proxies, for example 'https://www.google.com'
    :return: status check list with proxies and check results
    """
    art.tprint('PyScientist proxy-checker')

    # Initially test blank proxy to be sure that internet connection to the host can be established without proxy
    print('{:~^120}'.format(''))
    print('{:~^120}'.format(''))
    print('{:~^120}'.format(f'The testing started at {datetime.datetime.now()}'))
    print('{:~^120}'.format(''))
    print('{:~^120}'.format(''))
    blank_roxy_result = test_single_proxy(proc_host, '')
    proxies_status_check = [proc_proxies_list, [test_single_proxy(proc_host, proxy) for proxy in proc_proxies_list]]
    # Print results of testing for group of proxies
    print('{:~^120}'.format(''))
    print('{:~^120}'.format(''))
    print(f'Without proxy the following results were get \n'
          f'(status code, availability, duration of request in seconds, current date, host) \n'
          f'{blank_roxy_result}')
    print('{:~^120}'.format(''))
    print('{:~^120}'.format(''))
    print(f'proxy - (status code, availability, duration of request in seconds, current date, host)')
    [print(f'{proxies_status_check[0][i]} - {proxies_status_check[1][i]}')
        for i in range(0, len(proxies_status_check[0]))]
    print('{:~^120}'.format(''))
    print('{:~^120}'.format(''))
    print('{:~^120}'.format(f'The testing finished at {datetime.datetime.now()}'))
    print('{:~^120}'.format(''))
    print('{:~^120}'.format(''))
    return proxies_status_check


if __name__ == '__main__':
    #host = 'http://www.httpbin.org/ip'  # http host
    #host = 'https://www.google.com'
    host = 'https://mir-kvestov.ru'  # https host
    proxies_list = load_proxies()
    proxies_status_check = group_proxies_testing(proxies_list, host)
    write_check_results_to_file(proxies_status_check)



