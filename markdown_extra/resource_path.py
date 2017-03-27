"""This extension allows to perform various operation on local paths.

This extensions does two things.
First, it extracts local path from tags, resolves them to absolute path.

Extracted paths are then stored in a ``local_paths`` attribute of markdown
in the form of a list of tuples.
Each tuple has two element: the absolute path of the resources and the
formatted path.
"""

try:
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class ResourcePathTreeProcessor(Treeprocessor):
    def __init__(self, md, resource_tags, root_path):
        self.md = md
        self.resource_tags = resource_tags
        self.root_path = root_path
        super(ResourcePathTreeProcessor, self).__init__(md)

    def run(self, root):
        self.md.resource_path = []

        for tag_name, attr_name in self.resource_tags:
            for tag in root.findall(tag_name):
                path = tag.get(attr_name)
                # do not process this if no tag are given
                if path is None:
                    continue
                parsed = urlparse(path)
                if parsed.scheme or parsed.path.startswith('/'):
                    continue
                new_path = urljoin(self.root_path, path)
                self.md.resource_path.append((path, new_path))
                tag.set(attr_name, new_path)


class ResourcePathExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'root_path': [None, "The root path to resolve resources"],
            'resource_tags': [(('a', 'href'), ('img', 'src')), ''],
        }
        super(ResourcePathExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add(
            'resource_path',
            ResourcePathTreeProcessor(
                md,
                resource_tags=self.getConfig('resource_tags'),
                root_path=self.getConfig('root_path')),
            '_end')


def makeExtension(**kwargs):
    return ResourcePathExtension(**kwargs)
