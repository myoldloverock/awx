# Copyright (c) 2016 Ansible, Inc.
# All Rights Reserved.

# Python
import pytest

# Django
from django.core.urlresolvers import reverse

# AWX
from awx.conf.models import Setting


@pytest.mark.django_db
def test_license_cannot_be_removed_via_system_settings(get, put, patch, delete, admin, enterprise_license):
    url = reverse('api:setting_singleton_detail', args=('system',))
    response = get(url, user=admin, expect=200)
    assert not response.data['LICENSE']
    Setting.objects.create(key='LICENSE', value=enterprise_license)
    response = get(url, user=admin, expect=200)
    assert response.data['LICENSE']
    put(url, user=admin, data=response.data, expect=200)
    response = get(url, user=admin, expect=200)
    assert response.data['LICENSE']
    patch(url, user=admin, data={}, expect=200)
    response = get(url, user=admin, expect=200)
    assert response.data['LICENSE']
    delete(url, user=admin, expect=204)
    response = get(url, user=admin, expect=200)
    assert response.data['LICENSE']