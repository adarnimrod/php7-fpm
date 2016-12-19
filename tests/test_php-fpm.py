from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_php_fpm_service(Service, SystemInfo, File):
    if SystemInfo.type == 'openbsd':
        service = Service('php56_fpm')
        socket = File('/var/www/run/php-fpm.sock')
        user = 'www'
    elif SystemInfo.type == 'linux' and SystemInfo.distribution in ['debian',
                                                                    'ubuntu']:
        service = Service('php5-fpm')
        socket = File('/var/run/php5-fpm.sock')
        user = 'www-data'
    assert socket.is_socket
    assert socket.mode == 0o0660
    assert socket.user == user
    assert socket.group == user
    assert service.is_running
    try:
        assert service.is_enabled
    except NotImplementedError:
        pass


def test_phpinfo(Command):
    'PHP Version 5' in Command('curl http://localhost/phpinfo.php').stdout


def test_php_fpm_config(Command, Sudo, SystemInfo):
    with Sudo():
        if SystemInfo.type == 'openbsd':
            assert Command('php-fpm-5.6 -t').rc == 0
        elif SystemInfo.type == 'linux' and SystemInfo.distribution in [
                'debian', 'ubuntu'
        ]:
            assert Command('php5-fpm -t').rc == 0
