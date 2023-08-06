import itertools

import numpy as np

from shyft.dashboard.apps.water_route_app.mock_water_route import WaterRoute
from shyft.util.layoutgraph import WaterRouteGraph, ghost_object_factory


class BasicWaterRouteGraph(WaterRouteGraph):
    def generate_graph(self, water_course):
        """

        Parameters
        ----------
        water_course

        Returns
        -------

        """
        self.dh_tag_obj = self.get_clean_dh_tag_obj()
        self.dh_tag_obj['reservoirs'] = {res.tag: res for res in water_course.reservoirs.values()}
        self.dh_tag_obj['power_stations'] = {ps.tag: ps for ps in water_course.power_stations.values()}

        self.dh_tag_obj['main_water_routes'] = {res.tag: res for res in water_course.main_water_routes.values()}
        self.dh_tag_obj['spill_routes'] = {res.tag: res for res in water_course.spill_routes.values()}
        self.dh_tag_obj['bypass_routes'] = {res.tag: res for res in water_course.bypass_routes.values()}

        # 1. prepare all objects to be added and evaluate graph structure
        # 1.1 reservoirs and power stations
        node_objects = list(itertools.chain(self.dh_tag_obj['reservoirs'].values(),
                                            self.dh_tag_obj['power_stations'].values()))
        # 1.2 all water_routes
        edge_objects = list(itertools.chain(self.dh_tag_obj['main_water_routes'].values(),
                                            self.dh_tag_obj['spill_routes'].values(),
                                            self.dh_tag_obj['bypass_routes'].values()))

        object_layout_keys = ['Reservoir']*len(self.dh_tag_obj['reservoirs'])
        object_layout_keys.extend(['PowerStation'] * len(self.dh_tag_obj['power_stations']))

        # check if extra nodes are needed to add, and define start and end node lists
        start_objects = np.empty(len(edge_objects), dtype=object)
        end_objects = np.empty(len(edge_objects), dtype=object)
        oceans = []
        ocean_counter = 0
        spill_oceans = []
        spill_ocean_cluster = []
        spill_ocean_config = []

        connections_dict = {}

        for i, obj in enumerate(edge_objects):
            # check for ocean and number of connections

            # connection to ocean
            start_objects[i] = obj.upstreams[0].target
            if not obj.downstreams:  # Reached the ocean
                ocean_counter += 1
                ocean = ghost_object_factory('Ocean', f"Ocean_{obj.tag}_{ocean_counter}")
                end_objects[i] = ocean
                if isinstance(obj, WaterRoute):
                    oceans.append(ocean)
                    self.dh_tag_obj['oceans'][ocean.tag] = ocean
                else:
                    spill_ocean_cluster.append(ghost_object_factory('GraphSpillOcean',
                                                                    f'Spill_Ocean_Cluster_{ocean_counter}'))
                    spill_oceans.append([obj.upstreams[0].target, ocean])
                    self.dh_tag_obj[f'oceans_{obj.upstream_role.name}'][ocean.tag] = ocean

                    config_key = obj.upstreams[0].target.__class__.__name__
                    spill_ocean_config.append([config_key, 'OceanSpill'])
            else:
                end_objects[i] = obj.downstreams[0].target

        # 2. Add all objects to the graph
        # 2.1 Add all containers/nodes
        self.add_container(node_objects, object_layout_keys)

        # 2.2 Define all subgraphs (forced horizontal alignment)
        # create ocean subgraph
        ocean_subgraph_obj = ghost_object_factory('GraphOcean', 'Ocean_Subgraph')
        ocean_subgraph = self.add_subgraph(ocean_subgraph_obj, 'GraphOcean')
        # add containers to the ocean subgraph
        ocean_subgraph.add_container(oceans, ['Ocean']*len(oceans))

        # 2.3 Define all subgraphs (forced vertical alignment)
        for cluster_obj, node_objects, config in zip(spill_ocean_cluster, spill_oceans, spill_ocean_config):
            cluster_container = self.add_subgraph(cluster_obj, None)
            cluster_container.add_container(node_objects, config)

        # 2.4 Add all edges/connections
        self.add_connections(edge_objects, start_objects, end_objects,  [obj.upstream_role.name for obj in edge_objects])

        # 3.0 Generate graph coordinates
        self.generate_graph_coordinates()
