import unittest

from .context.network_benchmark.core import LatencyBenchmark


class PingTest(unittest.TestCase):
    gdns = {'name': '8.8.8.8', 'alias': 'googleDNS'}
    g = {'name': 'google.com', 'alias': 'google'}

    def testPingNoDNS(self):
        assert LatencyBenchmark(servers=[PingTest.gdns]) is not None

    def testPingNoDNSCustomTimeout(self):
        assert LatencyBenchmark(servers=[PingTest.gdns],
                                timeout_in_sec=300) is not None

    def testPingDNS(self):
        assert LatencyBenchmark(servers=[PingTest.g]) is not None

    def testPingDNSCustomTimeout(self):
        assert LatencyBenchmark(servers=[PingTest.g],
                                timeout_in_sec=300) is not None

    def testPingWrongDNS(self):
        try:
            assert LatencyBenchmark(servers=[{'name': 'google.cXXXXom',
                                              'alias': 'google_fake'}]) \
                   is not None
        except IndexError:
            pass
        except Exception as e:
            self.fail('Failed with exception: ' + str(e))

    def testPingWrongNoDNS(self):
        try:
            assert LatencyBenchmark(servers=[
                {
                    'name': '256.232.111.0',
                    'alias': 'google_fake'
                }
            ]) is not None
        except IndexError:
            pass
        except Exception as e:
            self.fail('Failed with exception: ' + str(e))


if __name__ == '__main__':
    unittest.main()
