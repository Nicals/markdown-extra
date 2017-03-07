Extensions
==========

Meta
----

This extension adds metadata support inside markdown documents.

Metadata is a ``YAML`` formatted datastructure defined at the very beginning
of the document.
It must be defined between ``---`` YAML separators.
The first ``---`` must be the first line of the document to be correctly parsed.

Once the document is parsed, the metadata is save as a ``meta`` property of
the markdown instance used to convert the file.


.. doctest::

    >>> import markdown
    >>> md_content = """---
    ...
    ...     author: "John Doe"
    ...     tags:
    ...       - "first-tag"
    ...       - "other-tag"
    ...
    ... ---
    ...
    ... First paragraph of the document goes here
    ... """
    >>> md = markdown.Markdown(extensions=['markdown_extra.meta'])
    >>> html = md.convert(md_content)
    >>> md.meta['author']
    'John Doe'
    >>> md.meta['tags']
    ['first-tag', 'other-tag']


Summary
-------

This extension is used to extract a summary from a markdown file.

A summary is a paragraph tagged with a ``[summary]`` element in its first line.
The summary won't be rendered in the final HTML document.
After the parsing occures, the summary can be accessed in a ``summary``
property of the markdown instance used.

This first paragraph will not be rendered.


.. doctest::

    >>> import markdown
    >>> md_content = """
    ... [summary]
    ... This is the summary.
    ... It says very important stuff.
    ...
    ... This is the first paragraph of the document.
    ... """
    >>> md = markdown.Markdown(extensions=['markdown_extra.summary'])
    >>> md.convert(md_content)
    '<p>This is the first paragraph of the document.</p>'
    >>> md.summary
    'This is the summary.\nIt says very important stuff.'

If no ``summary`` tag is found in the document, the first paragraph will be
set in the ``summary`` property of the markdown instance.
In this case, the paragraph will not be removed from the final HTML produced.
