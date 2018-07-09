import os
import pathlib
from unittest import TestCase
from xml.etree import ElementTree

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from lxml import etree

from xunitparserx import parse
import xunitparserx


class X(object):
    def setUp(self):
        with open(os.path.join('tests', self.FILENAME)) as f:
            # the lib already does some sanity checks;
            # passing this is already a good test in itself
            self.ts, self.tr = parse(f)

    def test_results(self):
        """ check some expected results """
        for test in self.ts:
            if test.basename == 'ArteTest':
                assert test.good
                assert test.skipped
                assert test.time is not None
            if test.basename == 'YouTubeTest':
                assert test.good
                assert not test.skipped
            if test.basename == 'PastebinTest':
                assert not test.skipped
                if test.methodname == 'test_post':
                    assert test.bad
                    assert 'backend.pastebin_loggedin' in test.message
                    assert 'python2.7' in test.trace
                    assert 'exceptions.AssertionError' in test.alltext
                    assert 'exceptions.AssertionError' not in test.message
                    assert 'backend.pastebin_loggedin' in test.alltext
                    assert 'python2.7' in test.alltext
            if test.methodname == '003-passed-test':
                assert "testcase system output" in test.stdall
                assert "testcase error output" in test.stdall
                assert "testcase system output" in test.stdout
                assert "testcase error output" in test.stderr
                assert "testsuite system output" in self.ts.stdout
                assert "testsuite error output" in self.ts.stderr

    def test_hashes(self):
        """ assert hashes are unique """
        assert len(list(hash(t) for t in self.ts)) == len(set(hash(t) for t in self.ts))

    def test_testresult(self):
        if self.FILENAME in ('test1.xml', 'test2.xml', 'test3.xml', 'test4.xml'):
            assert len(self.tr.failures)
        else:
            assert not len(self.tr.failures)
        for f in self.tr.failures:
            if 'pastebin.test.PastebinTest' in repr(f[0]):
                assert 'backend.pastebin_loggedin' in f[1]

    def test_classname(self):
        for test in self.ts:
            assert test.classname


class Test1(X, TestCase):
    FILENAME = 'test1.xml'

    def test_notime(self):
        assert self.tr.time is None

    def test_name(self):
        assert self.ts.name == 'nosetests'

    def test_numbers(self):
        assert self.tr.testsRun == 104

class Test1_PLUS(X, TestCase):
    FILENAME = 'test1.xml'

    def test_from_string(self):
        import pathlib
        ts, tr=xunitparserx.fromstring( (pathlib.Path('tests')/self.FILENAME).read_text(encoding='utf-8'))
        assert str(tr) == str(self.tr)
        assert str(ts) == str(self.ts)
        pass

    pass


class Test2(X, TestCase):
    FILENAME = 'test2.xml'

    def test_time(self):
        assert self.tr.time is not None
        assert str(self.tr.time).startswith('0:00:05.')


class Test3(X, TestCase):
    FILENAME = 'test3.xml'

    def test_msg(self):
        for f in self.tr.failures:
            if len(f[1]):
                assert 'foo.py' in f[1]
                assert 'foo.py' in f[0].trace
                assert 'AssertionError' == f[0].typename
                assert 'AssertionError' in f[1]
                assert 'None' not in f[1]
                assert f[0].message is None


class Test4(X, TestCase):
    FILENAME = 'test4.xml'

    def test_props(self):
        assert self.ts.properties['assert-passed'] == '1'

    def test_name_has_been_parsed_within_testsuites(self):
        assert self.ts.name == 'base_test_1'

    def test_testsuite_package_has_been_parsed(self):
        assert self.ts.package == 'testdb'


class Test5(X, TestCase):
    FILENAME = 'test5.xml'

    def test_message(self):
        found = False
        for test in self.ts:
            if test.bad:
                assert test.errored
                assert 'The step timed out' in test.message
                assert 'PathToMyProject' in test.trace
                found = True
        assert found


class Test6(X, TestCase):
    FILENAME = 'test6.xml'


class Test7(X, TestCase):
    FILENAME = 'test7.xml'


class Test8(X, TestCase):
    FILENAME = 'test8.xml'

    def test_bad_suite_time(self):
        assert self.tr.time is None


class Test9(X, TestCase):
    FILENAME = 'test9_with_record_xml_property.xml'

    def test_prop_parse(self):
        for tc in self.ts: # type: xunitparserx.XUnitParserXTestCase
            if tc.basename == 'TestCustomMetadataInjection':
                assert tc.props is not None
                assert tc.props['assertions'] == 'REQ-1234, REQ-5678, REQ-9101'
                pass

        pass


    pass

class Test10(TestCase):
    FILENAME = 'test10_trx_sample.trx'

    def get_test_file_path(self):
        return str(pathlib.Path(__file__).parent/ 'tests'/ self.FILENAME)

    def test_xunitparserx_trx_to_mstest_convert(self):
        trx_source_str=pathlib.Path(self.get_test_file_path()).read_text(encoding='utf-8')

        #no throw means succ!
        result=xunitparserx.convert_mstest_trx_to_junit(trx_source_str)

        pass

    def test_xunitparserx_trx_parser(self):
        trx_source_str=pathlib.Path(self.get_test_file_path()).read_text(encoding='utf-8')
        ts, tr=xunitparserx.fromstring_trx(trx_source_str)
        assert ts is not None
        assert tr is not None

    pass


class OtherTestCase(TestCase):
    def test_xslt_api(self):
        xslt_root = etree.XML('''\
        <xsl:stylesheet version="1.0"
          xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
          <xsl:template match="/">
            <foo><xsl:value-of select="/a/b/text()" /></foo>
          </xsl:template>
        </xsl:stylesheet>''')
        transform = etree.XSLT(xslt_root)

        f = StringIO('<a><b>Hello World!</b></a>')
        doc = etree.parse(f)
        result_tree = transform(doc)

        root = etree.XML('<a><b>Text</b></a>')
        result = transform(root)
        xml = str(result)

        # not throw means succ
        pass

    pass