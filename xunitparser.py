import unittest
from xml.etree import ElementTree
from datetime import timedelta


def to_timedelta(val):
    if val is None:
        return None
    return timedelta(seconds=float(val))


class TestResult(unittest.TestResult):
    def _exc_info_to_string(self, err, test):
        err = (e for e in err if e)
        return ': '.join(err)


class TestCase(unittest.TestCase):
    TR_CLASS = TestResult

    def __init__(self, classname, methodname):
        super(TestCase, self).__init__()
        self.classname = classname
        self.methodname = methodname

    def __str__(self):
        return "%s (%s)" % (self.methodname, self.classname)

    def __repr__(self):
        return "<%s testMethod=%s>" % \
               (self.classname, self.methodname)

    def __hash__(self):
        return hash((type(self), self.classname, self.methodname))

    def id(self):
        return "%s.%s" % (self.classname, self.methodname)

    def seed(self, result, typename=None, message=None, trace=None):
        """ Provide the expected result """
        self.result, self.typename, self.message, self.trace = result, typename, message, trace

    def run(self, tr=None):
        """ Fake run() that produces the seeded result """
        tr = tr or self.TR_CLASS()

        tr.startTest(self)
        if self.result == 'success':
            tr.addSuccess(self)
        elif self.result == 'skipped':
            tr.addSkip(self, '%s: %s' % (self.typename, self._textMessage()))
        elif self.result == 'error':
            tr.addError(self, (self.typename, self._textMessage()))
        elif self.result == 'failure':
            tr.addFailure(self, (self.typename, self._textMessage()))
        tr.stopTest(self)

        return tr

    def _textMessage(self):
        msg = (e for e in (self.message, self.trace) if e)
        return '\n\n'.join(msg) or None

    @property
    def alltext(self):
        err = (e for e in (self.typename, self.message) if e)
        err = ': '.join(err)
        txt = (e for e in (err, self.trace) if e)
        return '\n\n'.join(txt) or None

    def setUp(self):
        """ Dummy method so __init__ does not fail """
        pass

    def tearDown(self):
        """ Dummy method so __init__ does not fail """
        pass

    def runTest(self):
        """ Dummy method so __init__ does not fail """
        self.run()

    @property
    def basename(self):
        return self.classname.rpartition('.')[2]

    @property
    def success(self):
        return self.result == 'success'

    @property
    def skipped(self):
        return self.result == 'skipped'

    @property
    def failed(self):
        return self.result == 'failure'

    @property
    def errored(self):
        return self.result == 'error'

    @property
    def good(self):
        return self.skipped or self.success

    @property
    def bad(self):
        return not self.good


class TestSuite(unittest.TestSuite):
    pass


class Parser(object):
    TC_CLASS = TestCase
    TS_CLASS = TestSuite
    TR_CLASS = TestResult

    def parse(self, source):
        ts = self.TS_CLASS()

        xml = ElementTree.parse(source)
        root = xml.getroot()
        assert root.tag == 'testsuite'
        for el in xml.getroot():
            if el.tag == 'testcase':
                if len(el) == 0:
                    tc = self.TC_CLASS(el.attrib['classname'], el.attrib['name'])
                    tc.seed('success', trace=el.text or None)
                    tc.time = to_timedelta(el.attrib.get('time'))
                    ts.addTest(tc)
                for e in el:
                    if e.tag in ('failure', 'error', 'skipped'):
                        result = e.tag
                        typename = e.attrib.get('type')
                        message = e.attrib.get('message')
                        tc = self.TC_CLASS(el.attrib['classname'], el.attrib['name'])
                        tc.seed(result, typename, message, e.text or None)
                        tc.time = to_timedelta(el.attrib.get('time'))
                        ts.addTest(tc)
        tr = ts.run(self.TR_CLASS())

        ts.name = root.attrib.get('name')
        tr.time = to_timedelta(root.attrib.get('time'))

        # check totals if they are in the root XML element
        if 'errors' in root.attrib:
            assert len(tr.errors) == int(root.attrib['errors'])
        if 'failures' in root.attrib:
            assert len(tr.failures) == int(root.attrib['failures'])
        if 'skip' in root.attrib:
            assert len(tr.skipped) == int(root.attrib['skip'])
        if 'tests' in root.attrib:
            assert len(list(ts)) == int(root.attrib['tests'])

        return (ts, tr)


def parse(source):
    return Parser().parse(source)
