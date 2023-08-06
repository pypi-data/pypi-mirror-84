class ProductionNode(object):

    def __init__(self, tag, name, ups=None, downs=None):
        self.tag = str(tag)
        self.name = name
        self.id = tag
        self.ups = ups or []
        self.downs = downs or []

    def update_references(self, reference_dict):
        """ replace ids in ups and downs with
        objects from refernce list"""

        new_ups = []
        for ref in self.ups:
            if type(ref) == int:
                if ref in reference_dict.keys():
                    new_ups.append(reference_dict[ref])
                else:
                    msg = f"Error: {self.__class__.__name__} {self.tag}: upstream object with id {ref} not found"
                    raise (ValueError(msg))
        new_downs = []
        for ref in self.downs:
            if type(ref) == int:
                if ref in reference_dict.keys():
                    new_downs.append(reference_dict[ref])
                else:
                    msg = f"Error: {self.__class__.__name__} {self.tag}: downstream object with id {ref} not found"
                    raise (ValueError(msg))
        self.downs = new_downs


class Reservoir(ProductionNode):
    def __init__(self, tag, name, ups, downs):
        super(Reservoir, self).__init__(tag, name, ups=ups, downs=downs)


class PowerStation(ProductionNode):
    def __init__(self, tag, name, ups, downs):
        super(PowerStation, self).__init__(tag, name, ups=ups, downs=downs)


class StreamObj:
    def __init__(self, target):
        self.target = target


class HydroConnection:

    def __init__(self, tag, name, source=None, target=None):
        self.tag = str(tag)
        self.name = name
        if not isinstance(target, list):
            target = [target]
        if not isinstance(source, list):
            source = [source]
        self.target = target
        self.source = source
        self.downstreams = []
        self.upstreams = []

    def update_references(self, reference_dict):
        """ replace ids in ups and downs with
        objects from refernce list"""

        for target in self.target:
            if type(target) == int:
                if target in reference_dict.keys():

                    self.downstreams.append(StreamObj(reference_dict[target]))
                else:
                    msg = "Error: {} {}: target object with id {} not found".format(self.__class__.__name__,
                                                                                    self.tag, target)
                    raise (ValueError(msg))

        for source in self.source:
            if type(source) == int:
                if source in reference_dict.keys():
                    self.upstreams.append(StreamObj(reference_dict[source]))
                else:
                    msg = "Error: {} {}: source object with id {} not found".format(self.__class__.__name__,
                                                                                    self.tag, source)
                    raise (ValueError(msg))


class UpstreamRole(object):
    def __init__(self, role):
        self.name = role


class WaterRoute(HydroConnection):
    def __init__(self, tag, name, source=None, target=None):
        super(WaterRoute, self).__init__(tag, name, source=source, target=target)
        self.upstream_role = UpstreamRole('main_water_flow')


class SpillRoute(HydroConnection):
    def __init__(self, tag, name, source=None, target=None):
        super(SpillRoute, self).__init__(tag, name, source=source, target=target)
        self.upstream_role = UpstreamRole('flood')


class BypassRoute(HydroConnection):
    def __init__(self, tag, name, source=None, target=None):
        super(BypassRoute, self).__init__(tag, name, source=source, target=target)
        self.upstream_role = UpstreamRole('bypass')


class HydroPowerSystem(object):

    def __init__(self,
                 reservoirs=None,
                 power_stations=None,
                 main_water_routes=None,
                 spill_routes=None,
                 bypass_routes=None):

        self.reservoirs = reservoirs or {}
        self.power_stations = power_stations or {}

        self.main_water_routes = main_water_routes or {}
        self.spill_routes = spill_routes or {}
        self.bypass_routes = bypass_routes or {}

        nodes = {**self.reservoirs, **self.power_stations}
        connections = {**self.main_water_routes, **self.spill_routes, **self.bypass_routes}

        for reservoir in self.reservoirs.values():
            reservoir.update_references(connections)

        for power_station in self.power_stations.values():
            power_station.update_references(connections)

        for water_route in self.main_water_routes.values():
            reference_dict = self.main_water_routes.copy()
            reference_dict.update(nodes)
            water_route.update_references(reference_dict)

        for water_route in self.spill_routes.values():
            water_route.update_references(self.reservoirs)

        for water_route in self.bypass_routes.values():
            water_route.update_references(self.reservoirs)


def generate_hydro_power_system():
    reservoirs = {1: Reservoir(1, 'Reservoir A', ups=[], downs=[2, 15]),
                  3: Reservoir(3, 'Reservoir B', ups=[2, 16, 20], downs=[4]),
                  5: Reservoir(5, 'Reservoir C', ups=[24], downs=[6]),
                  7: Reservoir(7, 'Reservoir D', ups=[], downs=[8, 16]),
                  9: Reservoir(9, 'Reservoir E', ups=[14, 17, 23], downs=[10]),
                  11: Reservoir(11, 'Reservoir F', ups=[], downs=[12, 17]),
                  13: Reservoir(13, 'Reservoir G', ups=[], downs=[14, 18])}
    power_stations = {19: PowerStation(19, 'Power Station A', ups=[8], downs=[20]),
                      21: PowerStation(21, 'Power Station B', ups=[12], downs=[23]),
                      22: PowerStation(22, 'Power Station C', ups=[4, 10], downs=[24])}
    main_water_routes = {2: WaterRoute(2, 'main water way: R-A to R-B', source=1, target=3),
                         4: WaterRoute(4, 'main water way: R-B to PS-C', source=3, target=22),
                         6: WaterRoute(6, 'main water way: R-C to ocean', source=5, target=None),
                         8: WaterRoute(8, 'main water way: R-D to PS-A', source=7, target=19),
                         10: WaterRoute(10, 'main water way: R-E to PS-C', source=9, target=22),
                         12: WaterRoute(12, 'main water way: R-F to PS-B', source=11, target=21),
                         14: WaterRoute(14, 'main water way: R-G to R-E', source=13, target=9),
                         20: WaterRoute(20, 'main water way: PS-A to R-B', source=19, target=3),
                         23: WaterRoute(23, 'main water way:  PS-B to R-E', source=21, target=9),
                         24: WaterRoute(24, 'main water way:  PS-C to R-C', source=22, target=5)}
    spill_routes = {17: SpillRoute(17, 'Spill from R-F to R-E', source=11, target=9),
                    18: SpillRoute(18, 'Spill from R-G to ocean', source=13, target=None)}
    bypass_routes = {15: BypassRoute(15, 'Bypass from R-A to ocean', source=1, target=None),
                     16: BypassRoute(16, 'Bypass from R-D to R-B', source=7, target=3)}

    hps = HydroPowerSystem(reservoirs=reservoirs,
                           power_stations=power_stations,
                           main_water_routes=main_water_routes,
                           spill_routes=spill_routes,
                           bypass_routes=bypass_routes)

    return hps
