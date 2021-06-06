import shodan

def search(search, API_KEY, log):
    api = shodan.Shodan(API_KEY)
    open_instances = []

    try:
        #results = api.search(search, page=1)
        page_number = 1
        results = api.search(search, page=page_number)
        total_results = results['total']
        total_pages = round(total_results/100)
        #results = api.search(search, page=1)

        # need to caculate pages from here
        log.info('shodan total results: {0}'.format(total_results))
        log.info("processing page: {0} out of {1}".format(page_number,total_pages))

        #results = api.search(search, page=1)
        for page_number in range(2, total_pages):
            if page_number != 1:
                log.info("processing page: {0} out of {1}".format(page_number,total_pages))
                results = api.search(search, page=page_number)
                for r in results['matches']:
                    open_instance = dict()
                    log.debug("found matching {0}:{1}".format(r['ip_str'],r['port']))
                    open_instance ['ip'] = r['ip_str']
                    open_instance['port'] = r['port']
                    if 'domain' in r:
                        open_instance['domains'] = r['domain']
                    else:
                        open_instance['domains'] = ''
                        open_instance['hostnames'] = r['hostnames']
                        open_instance['timestamp'] = r['timestamp']
                        if 'ssl' in r:
                            open_instance['ssl'] = r['ssl']['cert']['subject']

                            #print ('{}'.format(open_instance))
                            open_instances.append(open_instance)
#                           print ('{} '.format(json.dumps(open_instance,indent=2)))

    except Exception as e:
        log.info('shodan search error: {}'.format(e))
    return open_instances
