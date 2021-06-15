import time
import requests

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0

site_url = ""
output = "output.txt"
input_list = "input_url_list.txt"


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                # print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        # print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
        # with open("links.txt", "w") as f:
        #     f.write(str(urls))
    return urls


def recursive_search(link, url_set=[]):
    bad_links = 0
    all_links = get_all_website_links(link)
    for url in all_links:
        try:
            with open(output, "a") as f:
                response = requests.get(url).status_code
                f.write(link + " | " + str(response) + " | " + url + "\n")
            if response != 200:
                bad_links += 1
            if url in url_set \
                    or link not in url \
                    or ".pdf" in url\
                    or "https:/t.me/" in url:
                continue
            time.sleep(0.2)
            url_set.append(url)
            recursive_search(url, url_set)
        except Exception as e:
            with open(output, "a") as f:
                f.write(link + " | " + "error" + " | " + url + "\n")
    if len(all_links) != 0:
        percentage_available_links = (1 - bad_links / len(all_links)) * 100
    else:
        percentage_available_links = 0
    return url_set, percentage_available_links


#
# def do_test():
#     with open(input_list) as f:
#         url_list = f.read().splitlines()
#     for site in url_list:
#         site_links = recursive_search(site)
#         print(site + str(len(site_links)))

