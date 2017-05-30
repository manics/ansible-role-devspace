import testinfra.utils.ansible_runner
from time import sleep

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_jenkins_8443(Command):
    # Although the containers are started they may not be ready to receive
    # connections, retry for 10 mins
    for n in xrange(1, 61):
        sleep(10)
        c = Command('curl -k https://localhost:8443/')
        if (c.rc == 0) and ('Dashboard [Jenkins]' in c.stdout):
            break
        print 'Still waiting after %d s' % (10 * n)
    assert c.rc == 0
    assert 'Dashboard [Jenkins]' in c.stdout
    assert 'OMERO-build' in c.stdout
