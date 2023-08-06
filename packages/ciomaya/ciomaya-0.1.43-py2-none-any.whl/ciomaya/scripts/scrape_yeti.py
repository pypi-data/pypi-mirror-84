from ciomaya.lib import software

"""
A scraper to collect paths from Yeti nodes.
"""
 

def run(_):
    ############# FOR NOW ###########
    if software.detect_yeti():
        raise NotImplementedError(
            "Yeti Asset Scraping is not yet implemented. To submit while the Yeti plugin is loaded, turn off the Yeti scraper in the Asset Scapers section. If you want to render yeti hair, we recommend you use the traditional client-tools submitter in the meantime.")
    return []
    #################################
