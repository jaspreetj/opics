import yaml as _yaml
import pathlib as _pathlib
from importlib import import_module
from opics.libraries.catalogue_mgmt import download_library, remove_library
import sys

_curr_dir = _pathlib.Path(__file__).parent.resolve()
catalogue = _curr_dir / "catalogue.yaml"

default_catalog = """
ebeam:
  dl_link: https://github.com/jaspreetj/opics_ebeam/archive/refs/tags/0.3.34.zip
  installed: false
  library_path:
  name: ebeam
  version: 0.3.34
"""


if not catalogue.exists():
    catalogue.write_text(default_catalog)
    print(f"write {catalogue!r}")

# read yaml file for available libraries in the catalogue
with open(_curr_dir / "catalogue.yaml", "r") as _stream:
    library_catalogue = _yaml.safe_load(_stream)


def _import_external_libraries(library_catalogue):
    installed_libraries = []

    for each_lib in library_catalogue.keys():

        if library_catalogue[each_lib]["installed"]:
            sys.path.append(f"{library_catalogue[each_lib]['library_path']}")
            installed_libraries.append(each_lib)
            globals()[each_lib] = import_module(each_lib)

    return installed_libraries


installed_libraries = _import_external_libraries(library_catalogue)

__all__ = [
    "download_library",
    "remove_library",
]


if __name__ == "__main__":
    import os
    import pathlib
    import opics as op

    home = pathlib.Path.home()
    cwd = pathlib.Path.cwd()
    dirpath = home / ".opics"

    installation_path = pathlib.Path(os.environ.get("USERPROFILE", dirpath))
    op.libraries.download_library("ebeam", str(installation_path))
