try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import xml.etree.ElementTree as ElementTree

from markdown_extra import summary


class TestSummaryPreprocessor:
    def test_removes_summary(self):
        preproc = summary.SummaryPreprocessor()
        preproc.md = Mock()

        lines = preproc.run(['foo', '', ' [summary] ', 'hello', '', 'bar'])

        assert lines == ['foo', '', 'bar']

    def test_sets_md_summary_to_none_if_no_tag(self):
        preproc = summary.SummaryPreprocessor()
        preproc.md = Mock()

        preproc.run(['foo', 'bar', '', 'baz'])

        assert preproc.md.summary is None

    def test_sets_md_summary_attribute(self):
        preproc = summary.SummaryPreprocessor()
        preproc.md = Mock()

        preproc.run(['foo', '', ' [summary] ', 'hello', 'world', '', 'bar'])

        assert preproc.md.summary == 'hello\nworld'


class TestSummaryTreeProcessor:
    def test_keeps_summary_if_already_set(self):
        treeproc = summary.SummaryTreeProcessor()
        treeproc.md = Mock(summary='foo')

        treeproc.run(ElementTree.fromstring('<html><p>Foo</p><p>Bar</p></html>'))

        assert treeproc.md.summary == 'foo'

    def test_uses_first_paragraph_if_no_summary(self):
        treeproc = summary.SummaryTreeProcessor()
        treeproc.md = Mock(summary=None)

        treeproc.run(ElementTree.fromstring('<html><p>Ham <a href="#">spam</a></p><p>Bar</p></html>'))

        assert treeproc.md.summary == 'Ham spam'

    def test_no_paragraph(self):
        treeproc = summary.SummaryTreeProcessor()
        treeproc.md = Mock(summary=None)

        treeproc.run(ElementTree.fromstring('<html><img src="Foo" /></html>'))

        assert treeproc.md.summary is None
