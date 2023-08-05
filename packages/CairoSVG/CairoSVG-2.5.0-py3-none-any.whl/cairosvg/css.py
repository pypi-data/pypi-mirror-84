"""
Handle CSS stylesheets.

"""

import cssselect2
import tinycss2

from .url import parse_url


def find_stylesheets(tree):
    """Find the stylesheets included in ``tree``."""
    # TODO: support contentStyleType on <svg>
    default_type = 'text/css'
    for element in tree.xml_tree.iter():
        # http://www.w3.org/TR/SVG/styling.html#StyleElement
        if (element.tag == '{http://www.w3.org/2000/svg}style' and
                element.get('type', default_type) == 'text/css' and
                element.text):
            # TODO: pass href for relative URLs
            # TODO: support media types
            # TODO: what if <style> has children elements?
            yield tinycss2.parse_stylesheet(
                element.text, skip_comments=True, skip_whitespace=True)


def find_stylesheets_rules(tree, stylesheet_rules, url):
    """Find the rules in a stylesheet."""
    for rule in stylesheet_rules:
        if rule.type == 'at-rule':
            if rule.lower_at_keyword == 'import' and rule.content is None:
                # TODO: support media types in @import
                url_token = tinycss2.parse_one_component_value(rule.prelude)
                if url_token.type not in ('string', 'url'):
                    continue
                css_url = parse_url(url_token.value, url)
                stylesheet = tinycss2.parse_stylesheet(
                    tree.fetch_url(css_url, 'text/css').decode('utf-8'))
                for rule in find_stylesheets_rules(
                        tree, stylesheet, css_url.geturl()):
                    yield rule
            # TODO: support media types
            # if rule.lower_at_keyword == 'media':
        if rule.type == 'qualified-rule':
            yield rule
        # TODO: warn on error
        # if rule.type == 'error':


def parse_declarations(input):
    normal_declarations = []
    important_declarations = []
    for declaration in tinycss2.parse_declaration_list(input):
        # TODO: warn on error
        # if declaration.type == 'error':
        if (declaration.type == 'declaration' and
                not declaration.name.startswith('-')):
            # Serializing perfectly good tokens just to re-parse them later :(
            value = tinycss2.serialize(declaration.value).strip()
            declarations = (
                important_declarations if declaration.important
                else normal_declarations)
            declarations.append((declaration.lower_name, value))
    return normal_declarations, important_declarations


def parse_stylesheets(tree, url):
    """Find and parse the stylesheets in ``tree``.

    Return two :class:`cssselect2.Matcher` objects,
    for normal and !important declarations.

    """
    normal_matcher = cssselect2.Matcher()
    important_matcher = cssselect2.Matcher()
    for stylesheet in find_stylesheets(tree):
        for rule in find_stylesheets_rules(tree, stylesheet, url):
            normal_declarations, important_declarations = parse_declarations(
                rule.content)
            for selector in cssselect2.compile_selector_list(rule.prelude):
                if (selector.pseudo_element is None and
                        not selector.never_matches):
                    if normal_declarations:
                        normal_matcher.add_selector(
                            selector, normal_declarations)
                    if important_declarations:
                        important_matcher.add_selector(
                            selector, important_declarations)
    return normal_matcher, important_matcher


def get_declarations(rule):
    """Get the declarations in ``rule``."""
    if rule.type == 'qualified-rule':
        for declaration in tinycss2.parse_declaration_list(
                rule.content, skip_comments=True, skip_whitespace=True):
            value = ''.join(part.serialize() for part in declaration.value)
            # TODO: filter out invalid values
            yield declaration.lower_name, value, declaration.important
