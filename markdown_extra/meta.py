"""This extensions adds some meta data support to markdown.

Some YAML formatted metadata can be added in a document.
The YAML content must be enclosed into '---' separators.
If some metadata are defined, the very first line of the document MUST
be the opening '---' separator.

.. code::

    ---
    author: "John Doe"
    tags:
        - first-tag
        - second-tag
    ---

    First paragraph of the document.

The metadata will not be rendered in the final HTML document.

The metadata will be set into a ``meta`` attribute of the markdown instance
used.
"""

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import yaml


__all__ = ['MetaExtension']


class MetaPreprocessor(Preprocessor):
    def run(self, lines):
        self.markdown.meta = None
        inside_meta = True
        meta = []
        new_lines = []

        if lines[0] != '---':
            return lines

        for line_nb, line in enumerate(lines):
            # skip first line as we already know it's the delimiter
            if line_nb == 0:
                continue

            # end of meta
            if line == '---':
                inside_meta = False
                continue

            if inside_meta:
                meta.append(line)
            else:
                # prevent appending empty lines following the meta header
                if new_lines or not (not line and not new_lines):
                    new_lines.append(line)

        self.markdown.meta = yaml.load('\n'.join(meta))

        return new_lines


class MetaExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add("yaml-meta", MetaPreprocessor(md), '>normalize_whitespace')


def makeExtension(*args, **kwargs):
    return MetaExtension(*args, **kwargs)
