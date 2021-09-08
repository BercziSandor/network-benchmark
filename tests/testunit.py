import unittest

import network_benchmark


class PingTest(unittest.TestCase):
    gdns = {'name': '8.8.8.8', 'alias': 'googleDNS'}
    g = {'name': 'google.com', 'alias': 'google'}

    def testPingNoDNS(self):
        assert network_benchmark.LatencyBenchmark(servers=[PingTest.gdns]) is not None

    def testPingNoDNSCustomTimeout(self):
        assert network_benchmark.LatencyBenchmark(servers=[PingTest.gdns],
                                                  timeout_in_sec=300) is not None

    def testPingDNS(self):
        assert network_benchmark.LatencyBenchmark(servers=[PingTest.g]) is not None

    def testPingDNSCustomTimeout(self):
        assert network_benchmark.LatencyBenchmark(servers=[PingTest.g], timeout_in_sec=300) is not None

    def testPingWrongDNS(self):
        try:
            assert network_benchmark.LatencyBenchmark(servers=[{'name': 'google.cXXXXom', 'alias':
                'google_fake'}]) is not None
        except IndexError:
            pass
        except Exception as e:
            self.fail('Failed with exception: ', e)

    def testPingWrongNoDNS(self):
        try:
            assert network_benchmark.LatencyBenchmark(servers=[{'name': '256.232.111.0', 'alias':
                'google_fake'}]) is not None
        except IndexError:
            pass
        except Exception as e:
            self.fail('Failed with exception: ', e)


if __name__ == '__main__':
    unittest.main()
