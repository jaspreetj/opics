#!/usr/bin/env python
# coding: utf-8

# # Network Concatenation
# 
# The results of OPICS Networks/Circuits can be concatenated together to build large networks. In this notebook, we will explore this use-case in more-depth using the example of a two-stage lattice filter.

# In[1]:


import opics as op
from opics.libraries import ebeam


# Let's create a mach-zehnder interferometer circuit, and call it `stage_1`.

# In[2]:


circuit1 = op.Network(network_id="stage_1")
circuit1.add_component(ebeam.BDC, component_id="bdc1")
circuit1.add_component(ebeam.BDC, component_id="bdc2")
circuit1.add_component(ebeam.Waveguide, params=dict(
    length=10e-6), component_id="wg1")
circuit1.add_component(ebeam.Waveguide, params=dict(
    length=9.93e-6), component_id="wg2")

circuit1.connect("bdc1", 2, "wg1", 0)
circuit1.connect("bdc1", 3, "wg2", 0)
circuit1.connect("bdc2", 0, "wg1", 1)
circuit1.connect("bdc2", 1, "wg2", 1)
circuit1 = circuit1.simulate_network()


# Let's create another mach-zehnder interferometer circuit, and call it `stage_2`.

# In[3]:


circuit2 = op.Network(network_id="stage_2")
circuit2.add_component(ebeam.BDC, component_id="bdc1")
circuit2.add_component(ebeam.BDC, component_id="bdc2")
circuit2.add_component(ebeam.Waveguide, params=dict(
    length=10e-6), component_id="wg1")
circuit2.add_component(ebeam.Waveguide, params=dict(
    length=10.08e-6), component_id="wg2")
circuit2.connect("bdc1", 2, "wg1", 0)
circuit2.connect("bdc1", 3, "wg2", 0)
circuit2.connect("bdc2", 0, "wg1", 1)
circuit2.connect("bdc2", 1, "wg2", 1)
circuit2 = circuit2.simulate_network()


# Let's create a root circuit and concatenate both networks 
# ```
#   .-------.         .-------.         .____.
# --|stage_1|---------|stage_2|---------|BDC | --
# --|_______|-- wg1 --|_______|-- wg2 --|____| --
# ```

# In[4]:


root = op.Network(network_id="root")

root.add_component(circuit1, circuit1.component_id)
root.add_component(circuit2, circuit2.component_id)

root.add_component(ebeam.Waveguide, params=dict(
    length=100.125e-6), component_id="wg1")
root.add_component(ebeam.Waveguide, params=dict(
    length=50e-6), component_id="wg2")

root.add_component(ebeam.BDC, component_id="bdc")

root.connect("stage_1", 2, "stage_2", 0)

root.connect("stage_1", 3, "wg1", 0)
root.connect("stage_2", 1, "wg1", 1)

root.connect("stage_2", 2, "bdc", 0)
root.connect("stage_2", 3, "wg2", 0)
root.connect("bdc", 1, "wg2", 1)
root.simulate_network()


# In[5]:


root.sim_result.plot_sparameters(show_freq=False, ports=[[2,0], [3,0]], interactive=True)

