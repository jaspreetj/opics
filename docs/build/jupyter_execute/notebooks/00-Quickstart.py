#!/usr/bin/env python
# coding: utf-8

# # OPICS Quickstart
#
# ## Installing from pypi
#
# The easiest way to install OPICS is using pip pypi:
#
# ```console
#
# pip install opics
#
# ```
#
# ## Installing from source
#
# Download the OPICS source code.
#
# ```console
#
# git clone https://github.com/jaspreetj/opics
#
# ```
#
# Install the OPICS package using ``pip``.
#
# ```console
#
# pip install -e ./opics
#
# ```
#
# Once the package is installed, it can be imported using:

# In[1]:


import opics


# ## OPICS Libraries
#
# ### Listing available libraries
# The package does not come with any component libraries pre-installed. You can select and download available libraries from the library catalogue.

# In[2]:


library_catalogue = opics.libraries.library_catalogue

print(f"Available Libraries: {[_ for _ in library_catalogue.keys()]} ")


# ### Downloading libraries
#
# The OPICS libraries are downloaded by passing in `library_name`, `library_url`, and `library_path` to the `libraries.download_library` module. The module returns `True` if the library is downloaded successfully.

# In[3]:


library = library_catalogue["ebeam"]


import os

installation_path = os.path.join(
    os.path.join(os.environ["USERPROFILE"]), "Desktop\\delete"
)

opics.libraries.download_library(
    library_name=library["name"],
    library_url=library["dl_link"],
    library_path=installation_path,
)

# reload libraries
import importlib

importlib.reload(opics.libraries)


# ### List installed libraries
#

# In[ ]:


opics.libraries.installed_libraries


# ### List library components

# In[ ]:


opics.libraries.ebeam.components_list


# ### Remove libraries
#
# Any of the installed libraries can be removed using the `libraries.remove_library` module.

# In[ ]:


opics.libraries.remove_library("ebeam")

importlib.reload(opics.libraries)

print(opics.libraries.installed_libraries)


# In[ ]:


# reinstall ebeam library
opics.libraries.download_library(
    library_name=library["name"],
    library_url=library["dl_link"],
    library_path=installation_path,
)

importlib.reload(opics.libraries)

print(opics.libraries.installed_libraries)
