import json

import lxml
from pyld.jsonld import prepend_base, parse_url, JsonLdError, _is_array


# This function is from pyld. Replaced hard coded `json.loads` with an arg.
def load_html(
    input,
    url,
    profile,
    options,
    parse_script_content=json.loads,
):
    """
    Load one or more script tags from an HTML source.
    Unescapes and uncomments input, returns the internal representation.
    Returns base through options

    :param input: the document to parse.
    :param url: the original URL of the document.
    :param profile: When the resulting `contentType` is `text/html` or `application/xhtml+xml`,
        this option determines the profile to use for selecting a JSON-LD script elements.
    :param requestProfile: One or more IRIs to use in the request as a profile parameter.
    :param options: the options to use.
        [base] used for setting returning the base determined by the document.
        [extractAllScripts] True to extract all JSON-LD script elements
        from HTML, False to extract just the first.

    :return: the extracted JSON.
    """
    document = lxml.html.fromstring(input)
    # potentially update options[:base]
    html_base = document.xpath('/html/head/base/@href')
    if html_base:
        # use either specified base, or document location
        effective_base = options.get('base', url)
        if effective_base:
            html_base = prepend_base(effective_base, html_base[0])
        options['base'] = html_base

    url_elements = parse_url(url)
    if url_elements.fragment:
        # FIXME: CGI decode
        id = url_elements.fragment
        element = document.xpath('//script[@id="%s"]' % id)
        if not element:
            raise JsonLdError(
                'No script tag found for id.',
                'jsonld.LoadDocumentError',
                {'id': id}, code='loading document failed')
        types = element[0].xpath('@type')
        if not types or not types[0].startswith('application/ld+json'):
            raise JsonLdError(
                'Wrong type for script tag.',
                'jsonld.LoadDocumentError',
                {'type': types}, code='loading document failed')
        content = element[0].text
        try:
            return parse_script_content(content)
        except Exception as cause:
            raise JsonLdError(
                'Invalid JSON syntax.',
                'jsonld.SyntaxError',
                {'content': content}, code='invalid script element', cause=cause)

    elements = []
    if profile:
        elements = document.xpath('//script[starts-with(@type, "application/ld+json;profile=%s")]' % profile)
    if not elements:
        elements = document.xpath('//script[starts-with(@type, "application/ld+json")]')
    if options.get('extractAllScripts'):
        result = []
        for element in elements:
            try:
                js = parse_script_content(element.text)
                if _is_array(js):
                    result.extend(js)
                else:
                    result.append(js)
            except Exception as cause:
                raise JsonLdError(
                    'Invalid JSON syntax.',
                    'jsonld.SyntaxError',
                    {'content': element.text}, code='invalid script element', cause=cause)
        return result
    elif elements:
        try:
            return parse_script_content(elements[0].text)
        except Exception as cause:
            raise JsonLdError(
                'Invalid JSON syntax.',
                'jsonld.SyntaxError',
                {'content': elements[0].text}, code='invalid script element', cause=cause)
    else:
        raise JsonLdError(
            'No script tag found.',
            'jsonld.LoadDocumentError',
            {'type': type}, code='loading document failed')
