from functools import reduce
from hestia_earth.schema import SchemaType, Bibliography

from .bibliography_apis.utils import has_key, is_enabled, unique_values, biblio_name, actor_name
from .bibliography_apis.crossref import extend_crossref
from .bibliography_apis.mendeley import extend_mendeley
from .bibliography_apis.wos import extend_wos


def is_node_of(node_type: SchemaType): return lambda node: node.get('type') == node_type.value


def update_source(source: dict, bibliographies: list):
    def update_key(key: str):
        value = source.get(key)
        biblio = next((x for x in bibliographies if value and value.get('title') == x.get('originalTitle')), None)
        if biblio:
            source[key] = {**source[key], **biblio}
            del source[key]['originalTitle']

            name = biblio.get('name', biblio.get('title'))
            if key == 'bibliography' and name:
                source['name'] = name

    update_key('bibliography')
    update_key('metaAnalysisBibliography')
    return source


def need_update_source(node: dict):
    def has_title(key: str): return key in node and 'title' in node.get(key)

    return is_node_of(SchemaType.SOURCE)(node) and (has_title('bibliography') or has_title('metaAnalysisBibliography'))


def update_sources(bibliographies: list):
    def update_single_source(node):
        if isinstance(node, list):
            return list(reduce(lambda p, x: p + [update_single_source(x)], node, []))
        elif isinstance(node, dict):
            node = update_source(node, bibliographies) if need_update_source(node) else node
            list(map(update_single_source, node.values()))
        return node
    return update_single_source


def update_biblio(node: dict):
    name = biblio_name(node.get('authors'), node.get('year'))
    return {**node, **{'name': name if name else node.get('name')}}


def update_actor(node: dict):
    name = actor_name(node)
    if name:
        node['name'] = name
    return node


UPDATE_NODE_TYPE = {
    SchemaType.BIBLIOGRAPHY.value: update_biblio,
    SchemaType.ACTOR.value: update_actor
}


def update_node(node):
    if isinstance(node, list):
        return list(reduce(lambda p, x: p + [update_node(x)], node, []))
    elif isinstance(node, dict):
        node_type = node.get('type')
        node = UPDATE_NODE_TYPE[node_type](node) if node_type in UPDATE_NODE_TYPE else node
        for key, value in node.items():
            node[key] = update_node(value)
    return node


def has_node_value(node: dict):
    def has_value(key: str):
        value = node.get(key)
        if isinstance(value, str) or isinstance(value, list):
            return len(value) > 0
        if isinstance(value, int):
            return value > 0
        return value is not None
    return has_value


def get_node_citation(node: dict):
    required = Bibliography().required
    required_values = list(filter(has_node_value(node), required))
    title = node.get('title', '')
    title = title if len(title) > 0 else None
    return None if len(required_values) == len(required) else title


def get_titles_from_node(node: dict):
    title = get_node_citation(node) if is_node_of(SchemaType.BIBLIOGRAPHY)(node) else None
    return list(set(reduce(lambda x, y: x + get_citations(y), node.values(), [] if title is None else [title])))


def get_citations(nodes):
    if isinstance(nodes, list):
        return list(set(reduce(lambda p, x: p + get_citations(x), nodes, [])))
    elif isinstance(nodes, dict):
        return get_titles_from_node(nodes)
    else:
        return []


def extend(content, **kwargs):
    nodes = content.get('nodes') if 'nodes' in content else []

    actors = []

    if has_key('mendeley_username', **kwargs):
        (authors, bibliographies) = extend_mendeley(sorted(get_citations(nodes)), **kwargs)
        actors.extend([] if authors is None else authors)
        nodes = list(map(update_sources(bibliographies), nodes))

    if has_key('wos_api_key', **kwargs) or (has_key('wos_api_user', **kwargs) and has_key('wos_api_pwd', **kwargs)):
        (authors, bibliographies) = extend_wos(sorted(get_citations(nodes)), **kwargs)
        actors.extend([] if authors is None else authors)
        nodes = list(map(update_sources(bibliographies), nodes))

    if is_enabled('enable_crossref', **kwargs):
        (authors, bibliographies) = extend_crossref(sorted(get_citations(nodes)), **kwargs)
        actors.extend([] if authors is None else authors)
        nodes = list(map(update_sources(bibliographies), nodes))

    # update all nodes except sources
    nodes = list(map(update_node, nodes))

    return {'nodes': unique_values(actors) + nodes}
