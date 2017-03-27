import markdown
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import xml.etree.ElementTree as ElementTree

from markdown_extra import resource_path


def test_default_options():
    md = markdown.Markdown(extensions=['markdown_extra.resource_path'])
    tree_proc = md.treeprocessors['resource_path']

    assert tree_proc.resource_tags == (('a', 'href'), ('img', 'src'))


def test_overrides_options():
    md = markdown.Markdown(
        extensions=['markdown_extra.resource_path'],
        extension_configs={
            'markdown_extra.resource_path': {'resource_tags': (('foo', 'bar'),)}})
    tree_proc = md.treeprocessors['resource_path']

    assert tree_proc.resource_tags == (('foo', 'bar'),)


def test_sets_extracts_path():
    md = Mock()
    tree = ElementTree.fromstring('<html><a href="foo/bar">baz</a></html>')
    tree_proc = resource_path.ResourcePathTreeProcessor(
        md,
        (('a', 'href'),),
        '/ham/spam/')
    tree_proc.run(tree)

    assert md.resource_path == [('foo/bar', '/ham/spam/foo/bar')]


def test_resolves_resource_path():
    tree = ElementTree.fromstring('<html><a href="foo/bar">baz</a></html>')
    tree_proc = resource_path.ResourcePathTreeProcessor(
        Mock(), (('a', 'href'),), '/ham/spam/')
    tree_proc.run(tree)

    assert tree.find('a').get('href') == '/ham/spam/foo/bar'


def test_absolute_path_are_ignored():
    md = Mock()
    tree = ElementTree.fromstring('<html><img src="/foo/bar" /></html>')
    tree_proc = resource_path.ResourcePathTreeProcessor(
        md, (('img', 'src'),), '/ham/spam')
    tree_proc.run(tree)

    assert md.resource_path == []


def test_uri_are_ignored():
    md = Mock()
    tree = ElementTree.fromstring('<html><img src="http://example.org/foo" /></html>')
    tree_proc = resource_path.ResourcePathTreeProcessor(
        md, (('img', 'src'),), '/ham/spam')
    tree_proc.run(tree)

    assert md.resource_path == []
