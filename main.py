import time
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

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
    for url in get_all_website_links(link):
        try:
            with open(output, "a") as f:
                f.write(link + " | " + str(requests.get(url).status_code) + " | " + url + "\n")
            if url in url_set \
                    or site not in url \
                    or ".pdf" in url\
                    or "https:/t.me/" in url:
                continue
            time.sleep(0.1)
            url_set.append(url)
            recursive_search(url, url_set)
        except Exception:
            with open(output, "a") as f:
                f.write(link + " | " + "error" + " | " + url + "\n")

    return url_set


with open(input_list) as f:
    url_list = f.read().splitlines()
for site in url_list:
    print(len(recursive_search(site)))