try:
    from unittest.mock import Mock
except ImportError:  # python2
    from mock import Mock

from markdown_extra import meta


class TestMetaPreprocessor:
    def test_sets_meta_to_none_if_no_meta(self):
        preproc = meta.MetaPreprocessor()
        preproc.markdown = Mock()

        preproc.run(['A paragraph'])

        assert preproc.markdown.meta is None

    def test_extracts_meta(self):
        preproc = meta.MetaPreprocessor()
        preproc.markdown = Mock

        preproc.run(['---', 'foo: bar', 'bar:', '    - baz', '---'])

        assert preproc.markdown.meta == {'foo': 'bar', 'bar': ['baz']}

    def test_removes_meta(self):
        preproc = meta.MetaPreprocessor()
        preproc.markdown = Mock()

        lines = preproc.run(['---', 'foo: bar', '---', '', 'Paragraph'])

        assert lines == ['Paragraph']


class TestInjectMeta:
    def test_injects_meta(self):
        metadata = {'foo': 'bar', 'ham': ['spam']}
        md_content = """---
foo: bar
---

And a paragraph
"""

        assert meta.inject_meta(md_content, metadata) == """---

foo: bar
ham:
- spam

---

And a paragraph
"""

    def test_injects_new_meta(self):
        metadata = {'foo': 'bar', 'ham': ['spam']}
        md_content = "A paragraph"

        assert meta.inject_meta(md_content, metadata) == """---

foo: bar
ham:
- spam

---

A paragraph
"""

    def test_inject_updated_meta(self):
        metadata = {'foo': 'bar', 'ham': 'spam'}
        md_content = """---
foo: foo
---

A paragraph
"""

        assert meta.inject_meta(md_content, metadata, update=True) == """---

foo: bar
ham: spam

---

A paragraph
"""

    def test_removes_meta(self):
        md_content = """---
foo: bar
---
A paragraph
"""

        assert meta.inject_meta(md_content, None) == "A paragraph"
