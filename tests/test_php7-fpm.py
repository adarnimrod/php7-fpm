from testinfra.utils.ansible_runner import AnsibleRunner
import json

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_php7_fpm_service(Service, SystemInfo, File, Sudo):
    if SystemInfo.type == 'openbsd':
        service = Service('php70_fpm')
        socket = File('/var/www/run/php-fpm.sock')
        user = 'www'
    elif SystemInfo.type == 'linux' and SystemInfo.distribution in [
            'debian', 'ubuntu'
    ]:
        service = Service('php7.0-fpm')
        socket = File('/run/php/php7.0-fpm.sock')
        user = 'www-data'
    with Sudo():
        assert socket.is_socket
        assert socket.mode == 0o0660
        assert socket.user == user
        assert socket.group == user
        assert service.is_running
        try:
            assert service.is_enabled
        except NotImplementedError:
            pass


def test_php7info(Command):
    assert 'PHP Version 7.0' in Command(
        'curl http://localhost/phpinfo.php').stdout


def test_php7_fpm_config(Command, Sudo, SystemInfo):
    with Sudo():
        if SystemInfo.type == 'openbsd':
            assert Command('php-fpm-7.0 -t').rc == 0
        elif SystemInfo.type == 'linux' and SystemInfo.distribution in [
                'debian', 'ubuntu'
        ]:
            assert Command('php-fpm7.0 -t').rc == 0


def test_php7_fpm_status(Command):
    status = json.loads(
        Command('curl http://localhost/status.php?json').stdout)
    assert status['pool'] == 'www'
    assert status['process manager'] == 'dynamic'


def test_php7_fpm_ping(Command):
    assert 'pong' in Command('curl http://localhost/ping.php').stdout
