

def dns_query(query="techoverflow.net", nameserver="1.1.1.1", qtype="A"):
    """
    Query a specific nameserver for:
    - An IPv4 address for a given hostname (qtype="A")
    - An IPv6 address for a given hostname (qtype="AAAA")
    
    Returns the IP address as a string
    """
    import dns.resolver
    
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [nameserver]
    answer = resolver.query(query, qtype)
     
    if len(answer) == 0:
        return None
    else:
        return str(answer[0])