# -*- coding: utf-8 -*-

import pytest
from cfme import test_requirements
from cfme.cloud.provider import CloudProvider
from cfme.fixtures import pytest_selenium as sel
import cfme.web_ui.toolbar as tb
from cfme.web_ui import ButtonGroup, form_buttons, Quadicon, fill
from utils.appliance.implementations.ui import navigate_to
from utils.providers import setup_a_provider as _setup_a_provider
from cfme.configure import settings  # NOQA
from cfme.cloud import instance  # NOQA

pytestmark = [pytest.mark.tier(3),
              test_requirements.settings]


gtl_params = {
    'Cloud Providers': CloudProvider,
    'Availability Zones': 'clouds_availability_zones',
    'Flavors': 'clouds_flavors',
    'Instances': 'clouds_instances',
    'Images': 'clouds_images'
}


def select_two_quads():
    count = 0
    for quad in Quadicon.all("cloud_prov", this_page=True):
        count += 1
        if count > 2:
            break
        fill(quad.checkbox(), True)


@pytest.fixture(scope="module")
def setup_a_provider():
    _setup_a_provider(prov_class="cloud", prov_type="openstack", validate=True, check_existing=True)


def set_view(group, button):
    bg = ButtonGroup(group)
    if bg.active != button:
        bg.choose(button)
        sel.click(form_buttons.save)


def reset_default_view(name, default_view):
    bg = ButtonGroup(name)
    sel.force_navigate("my_settings_default_views")
    if bg.active != default_view:
        bg.choose(default_view)
        sel.click(form_buttons.save)


def get_default_view(name):
    bg = ButtonGroup(name)
    pytest.sel.force_navigate("my_settings_default_views")
    default_view = bg.active
    return default_view


def set_and_test_default_view(group_name, view, page):
    default_view = get_default_view(group_name)
    set_view(group_name, view)
    if isinstance(page, basestring):
        sel.force_navigate(page)
    else:
        navigate_to(page, 'All', use_resetter=False)
    assert tb.is_active(view), "{} view setting failed".format(view)
    reset_default_view(group_name, default_view)


@pytest.mark.parametrize('key', gtl_params, scope="module")
def test_tile_defaultview(request, setup_a_provider, key):
    set_and_test_default_view(key, 'Tile View', gtl_params[key])


@pytest.mark.parametrize('key', gtl_params, scope="module")
def test_list_defaultview(request, setup_a_provider, key):
    set_and_test_default_view(key, 'List View', gtl_params[key])


@pytest.mark.parametrize('key', gtl_params, scope="module")
def test_grid_defaultview(request, setup_a_provider, key):
    set_and_test_default_view(key, 'Grid View', gtl_params[key])


def set_and_test_view(group_name, view):
    default_view = get_default_view(group_name)
    set_view(group_name, view)
    sel.force_navigate('clouds_instances')
    select_two_quads()
    tb.select('Configuration', 'Compare Selected items')
    assert tb.is_active(view), "{} setting failed".format(view)
    reset_default_view(group_name, default_view)


@pytest.mark.meta(blockers=[1394331])
def test_expanded_view(request, setup_a_provider):
    set_and_test_view('Compare', 'Expanded View')


@pytest.mark.meta(blockers=[1394331])
def test_compressed_view(request, setup_a_provider):
    set_and_test_view('Compare', 'Compressed View')


@pytest.mark.meta(blockers=[1394331])
def test_details_view(request, setup_a_provider):
    set_and_test_view('Compare Mode', 'Details Mode')


@pytest.mark.meta(blockers=[1394331])
def test_exists_view(request, setup_a_provider):
    set_and_test_view('Compare Mode', 'Exists Mode')
