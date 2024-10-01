# SPDX-License-Identifier: AGPL-3.0-or-later

from lxml import html
from searx.utils import (
    extract_text,
    eval_xpath,
)

about = {
    "website": 'https://filepursuit.com',
}
base_url = 'https://filepursuit.com'
paging = True


def request(query, params):
    params['url'] = f"{base_url}/pursuit?q={query}&type=all&startrow={(params.get('pageno', 1) - 1) * 50}"
    return params


def response(resp):
    results = []
    dom = html.fromstring(resp.text)

    for result in eval_xpath(dom, './/div[@class="row"]'):
        link_element = result.xpath('.//a')
        title_element = result.xpath('.//h5')

        if link_element and title_element:
            url = link_element[0].get('href')
            title = extract_text(title_element[0])

            results.append({
                'title': title,
                'url': f"{base_url}{url}",
            })

    return results
