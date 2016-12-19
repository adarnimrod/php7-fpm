from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_php_fpm_service(Service, SystemInfo):
    if SystemInfo.type == 'openbsd':
        service = Service('php56_fpm')
    elif SystemInfo.type == 'debian':
        service = Service('php5-fpm')
    assert service.is_running
    try:
        assert service.is_enabled
    except NotImplementedError:
        pass
