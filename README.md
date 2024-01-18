RDMO MeSH plugin
================

The dynamic MeSH optionset will query internal database tables for descriptors matching the user input. The plugin is meant to be used with RDMO's autocomplete field and its server-side search capabilities.

Please visit the [RDMO documentation](https://rdmo.readthedocs.io/en/latest/configuration/plugins.html#optionset-providers) for detailed information on plugin.


Setup
-----

Install the plugin in your RDMO virtual environment using pip (directly from GitHub):

```bash
pip install git+https://github.com/rdmorganiser/rdmo-plugins-mesh
```

Add the `rdmo_mesh` app to your `INSTALLED_APPS` in `config/settings/local.py`:

```python
from . import INSTALLED_APPS
INSTALLED_APPS = ['rdmo_mesh'] + INSTALLED_APPS
```

Add the plugin to the `OPTIONSET_PROVIDERS` in `config/settings/local.py`:

```python
OPTIONSET_PROVIDERS = [
    ...
    ('mesh', _('Medical Subject Headings (MeSH)'), 'rdmo_mesh.providers.MeSHProvider'),
]
```

Optionally, a REST API for the MeSH data can be activated by adding the following to `config/urls.py`:

```python
urlpatterns = [
    ...
    path('api/v1/mesh/', include('rdmo_mesh.urls')),  # before the regular RDMO API!
    path('api/v1/', include('rdmo.core.urls.v1')),
    ...
]
```

Add the locaton of the source xml files to `config/settings/local.py` as well:

```python
MESH_DESCRIPTOR_URL = 'ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/xmlmesh/desc2021.xml'
MESH_QUALIFIER_URL = 'ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/xmlmesh/qual2021.xml'
MESH_PATH = '/path/to/where/the/xml/files/are/store/locally'
```

Since the plugin uses its own models, run the migrations:

```bash
python manage.py migrate
```

Import the MeSH data:

```bash
python manage.py import_mesh
```

After restarting RDMO, the `MeSHProvider` should be selectable as a provider option for option sets. Those optionsets should be used with a question using the `autocomplete` widget.
