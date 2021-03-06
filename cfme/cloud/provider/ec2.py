from widgetastic.widget import View
from widgetastic_patternfly import Tab, Input, Button
from wrapanapi.ec2 import EC2System

from cfme.common.provider import DefaultEndpoint, DefaultEndpointForm
from cfme.common.provider_views import BeforeFillMixin
from cfme.services.catalogs.catalog_items import AmazonCatalogItem
from . import CloudProvider


class EC2Endpoint(DefaultEndpoint):
    """
     represents default Amazon endpoint (Add/Edit dialogs)
    """
    @property
    def view_value_mapping(self):
        return {}


class EC2EndpointForm(View):
    """
     represents default Amazon endpoint form in UI (Add/Edit dialogs)
    """
    @View.nested
    class default(Tab, DefaultEndpointForm, BeforeFillMixin):  # NOQA
        TAB_NAME = 'Default'

    @View.nested
    class smart_state_docker(Tab, BeforeFillMixin):  # NOQA
        TAB_NAME = 'SmartState Docker'

        username = Input(id='smartstate_docker_userid')
        password = Input(id='smartstate_docker_password')

        validate = Button('Validate')


class EC2Provider(CloudProvider):
    """
     BaseProvider->CloudProvider->EC2Provider class.
     represents CFME provider and operations available in UI
    """
    catalog_item_type = AmazonCatalogItem
    type_name = "ec2"
    mgmt_class = EC2System
    db_types = ["Amazon::CloudManager"]
    endpoints_form = EC2EndpointForm
    discover_name = "Amazon EC2"
    settings_key = 'ems_amazon'

    def __init__(
            self, name=None, endpoints=None, zone=None, key=None, region=None, region_name=None,
            appliance=None):
        super(EC2Provider, self).__init__(name=name, endpoints=endpoints,
                                          zone=zone, key=key, appliance=appliance)
        self.region = region
        self.region_name = region_name

    @property
    def view_value_mapping(self):
        """Maps values to view attrs"""
        return {
            'name': self.name,
            'prov_type': 'Amazon EC2',
            'region': self.region_name,
        }

    @classmethod
    def from_config(cls, prov_config, prov_key, appliance=None):
        """Returns the EC" object from configuration"""
        endpoint = EC2Endpoint(**prov_config['endpoints']['default'])
        return cls(name=prov_config['name'],
                   region=prov_config['region'],
                   region_name=prov_config['region_name'],
                   endpoints={endpoint.name: endpoint},
                   zone=prov_config['server_zone'],
                   key=prov_key,
                   appliance=appliance)

    @staticmethod
    def discover_dict(credential):
        """Returns the discovery credentials dictionary"""
        return {
            'username': getattr(credential, 'principal', None),
            'password': getattr(credential, 'secret', None),
            'confirm_password': getattr(credential, 'verify_secret', None)
        }
