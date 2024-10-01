# SPDX-License-Identifier: AGPL-3.0-or-later

from lxml import html
from searx.utils import (
    extract_text,
    eval_xpath,
)

about = {
    "website": 'https://filemood.com',
}
base_url = 'https://filemood.com'
paging = True


def request(query, params):
    params['url'] = f"{base_url}/result?q={query}&f={params.get('pageno', 1) * 20}"
    return params


def response(resp):
    results = []
    dom = html.fromstring(resp.text)

    for result in eval_xpath(dom, './/table'):
        link_element = result.xpath('.//a')
        if link_element:
            title = link_element[0].get('title')
            url = link_element[0].get('href')
        else:
            title = None
            url = None

        if url or title:
            results.append({
                'title': title,
                'url': f"{base_url}{url}"})

    return results
