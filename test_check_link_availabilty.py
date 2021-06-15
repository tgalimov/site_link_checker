from main import recursive_search
import pytest

site_url_list = [
    ["https://ai.innopolis.university",        100],
    ["https://apply.innopolis.university",     100],
    ["https://career.innopolis.university",    100],
    ["https://cdo.innopolis.university",       100],
    ["https://corporate.innopolis.university", 100],
    ["https://dovuz.innopolis.university",     100],
    ["https://edu.innopolis.university",       100],
    ["https://hotel.innopolis.university",     100],
    ["https://innopolis.university",           100],
    ["https://itschool.innopolis.university",  100],
    ["https://media.innopolis.university",     100],
    # ["https://old.innopolis.university",       100],
    ["https://robotics.innopolis.university",  100],
    ["https://stc.innopolis.university",       100],
]


@pytest.mark.parametrize("site, expected_percent", site_url_list)
def test_site_links_availability(site, expected_percent):
    check_site_links = recursive_search(site)
    assert check_site_links[1] == expected_percent
