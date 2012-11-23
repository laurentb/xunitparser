from xml.etree import ElementTree
import unittest


class TestResult(unittest.TestResult):
    def _exc_info_to_string(self, err, test):
        return '%s: %s' % err

    #classname = el.attrib['classname'].rpartition('.')


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

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def id(self):
        return "%s.%s" % (self.classname, self.methodname)

    def seed(self, result, typename=None, message=None):
        self._seed = (result, typename, message)

    def run(self, tr=None):
        tr = tr or self.TR_CLASS()
        result, typename, message = self._seed

        tr.startTest(self)
        if result == 'success':
            tr.addSuccess(self)
        elif result == 'skipped':
            tr.addSkip(self, '%s: %s' % (typename, message))
        elif result == 'error':
            tr.addError(self, (typename, message))
        elif result == 'failure':
            tr.addFailure(self, (typename, message))
        tr.stopTest(self)

        return tr

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def runTest(self):
        self.run()


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
                    tc.seed('success')
                    ts.addTest(tc)
                for e in el:
                    if e.tag in ('failure', 'error', 'skipped'):
                        result = e.tag
                        typename = e.attrib.get('type')
                        message = e.attrib.get('message')
                        tc = self.TC_CLASS(el.attrib['classname'], el.attrib['name'])
                        tc.seed(result, typename, message)
                        ts.addTest(tc)
        tr = ts.run(self.TR_CLASS())

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
