from OpenSSL import SSL
import socket
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',  # Do Not Track
    'Referer': 'https://www.google.com/',
}


def verify_ssl_certificate(hostname):
    # First, check if the site is accessible via HTTPS
    hostname = f"www.{hostname}"
    try:
        response = requests.get(hostname,headers=headers,verify=False ,timeout=5)
        if response.status_code >= 400:
            return 0
        else:
            return 1
            
    except Exception:
        return 0

    # Then, check the SSL certificate using pyOpenSSL
    # context = SSL.Context(SSL.TLS_CLIENT_METHOD)
    # context.set_verify(SSL.VERIFY_PEER, lambda conn, cert, errno, depth, ok: ok)
    # context.set_default_verify_paths()
    # try:
    #     sock = socket.create_connection((hostname, 443), timeout=5)
    #     ssl_conn = SSL.Connection(context, sock)
    #     ssl_conn.set_tlsext_host_name(hostname.encode())
    #     ssl_conn.set_connect_state()
    #     ssl_conn.do_handshake()
    #     cert = ssl_conn.get_peer_certificate()
    #     ssl_conn.close()
    #     sock.close()
    #     return 1 if cert is not None else 0
    # except Exception:
    #     return 0