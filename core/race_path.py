
from typing import Union, Tuple, List, NamedTuple
import math
from lxml import etree


# Coordinate will be immutable since it extends NamedTuple
class Coordinate(NamedTuple):
    lon: float
    lat: float


# https://www.movable-type.co.uk/scripts/latlong.html
# uses the haversine formula to calculate distance between two points
def distance_between_coords(c1: Coordinate, c2: Coordinate) -> float:

    def haversine1(delta_phi: float, phi1: float, phi2: float, delta_lambda: float) -> float:
        return math.sin(delta_phi / 2.0)**2 + (math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0)**2))

    r = 6.371e6 # Earth's radius in meters

    phi1 = c1.lat * math.pi / 180.0
    phi2 = c2.lat * math.pi / 180.0

    delta_phi = phi2 - phi1
    delta_lambda = (c2.lon - c1.lon) * math.pi / 180.0

    a = haversine1(delta_phi, phi1, phi2, delta_lambda)
    d = 2 * math.asin(math.sqrt(a)) * r

    return d


# PathPoint will be immutable since it extends NamedTuple
class PathPoint(NamedTuple):
    race_distance: float
    coordinate: Coordinate


class RacePath():

    def __init__(self):
        self.points: List[PathPoint] = [] # list of coords in the format (race_distance, Coordinate)
        self.race_length = 0.0 # length of the race in meters
        self.name = None


    # looks like it matches the solver to 3 decimal places which is pretty good
    def get_point_from_distance(self, distance: Union[float, int]) -> Coordinate:

        if len(self.points) == 0:
            raise Exception('Path not initialized.')

        if type(distance) != float and type(distance) != int:
            raise ValueError('`distance` must a float or an int')

        if distance < 0.0:
            raise ValueError('`distance` is negative.')
        elif distance > self.race_length:
            raise ValueError('`distance` is past the end of the race.')

        # use binary search to find the 2 closest coordinates
        upper = len(self.points) - 1
        lower = 0

        while upper - lower > 1:

            middle = (upper - lower) // 2 + lower

            if distance == self.points[middle].race_distance:
                return self.points[middle].coordinate

            if distance < self.points[middle].race_distance:
                upper = middle
            else:
                lower = middle

        lc = self.points[lower].coordinate
        uc = self.points[upper].coordinate

        # race distance between points
        diff = self.points[upper].race_distance - self.points[lower].race_distance

        # they are the same point
        if diff == 0:
            return self.points[upper].coordinate

        angular_distance = distance_between_coords(lc, uc) / 6.371e6 # distance / radius

        # fraction of the way between lc and uc
        f = ((distance - self.points[lower].race_distance) / diff)

        a = math.sin((1-f)*angular_distance) / math.sin(angular_distance)
        b = math.sin(f*angular_distance) / math.sin(angular_distance)

        constant = math.pi / 180.0

        phi1 = lc.lat * constant
        phi2 = uc.lat * constant
        lambda1 = lc.lon * constant
        lambda2 = uc.lon * constant

        x = a * math.cos(phi1) * math.cos(lambda1) + b * math.cos(phi2) * math.cos(lambda2)
        y = a * math.cos(phi1) * math.sin(lambda1) + b * math.cos(phi2) * math.sin(lambda2)
        z = a * math.sin(phi1) + b * math.sin(phi2)

        phi_i = math.atan2(z, math.sqrt(x**2 + y**2)) # latitude
        lambda_i = math.atan2(y, x) # longitude

        # convert back from radians to degrees
        return Coordinate(lambda_i / constant, phi_i / constant)


    # fast and accurate to within 1e-6 of a meter
    # this is actually crazy accurate, originally from the SolarRacer
    def get_distance_from_point(self, coordinate: Coordinate) -> float:

        def constrain(x, minn, maxn):
            return min(max(minn, x), maxn)

        # count >= 2
        # generate numbers in range [minn, maxn]
        def gen(minn, maxn, count):

            step = (maxn - minn) / (count-1)
            current = minn

            while current < maxn:
                yield current
                current += step
            yield maxn                

        least_dist = float('inf') # distance to the point on the path
        closest_race_dist = 0 # distance along the path

        length = self.race_length

        search_center = length // 2 # center of the search area
        search_size = length // 2 # distance away from the center to search

        points_per_range = 19 # this should be odd so that the closest point remains an option
        search_size_reduction_factor = 0.25
        max_iterations = 20

        for i in range(max_iterations):

            # create list of distances
            distances = list(gen(
                max(search_center-search_size, 0),
                min(search_center+search_size, length),
                points_per_range-1))

            for race_dist in distances:

                # get point for the given distance
                point = self.get_point_from_distance(race_dist)
                # get the distance between the point on the path and our current location
                dist = distance_between_coords(coordinate, point)

                # see if this is closer than what we have so far
                if dist < least_dist:
                    least_dist = dist
                    closest_race_dist = race_dist

            search_center = closest_race_dist # make the center the closest distance along the path
            search_size *= search_size_reduction_factor # reduce the search space

        return closest_race_dist


    def load_path(self, file_path: str) -> None:

        try:
            tree = etree.parse(file_path)
        except OSError as e:
            print(e)
            return None

        # parse the file
        xml = tree.getroot()
        doc = xml.find('Document', namespaces=xml.nsmap)
        folder = doc.find('Folder', namespaces=xml.nsmap)
        placemark = folder.find('Placemark', namespaces=xml.nsmap)
        linestring = placemark.find('LineString', namespaces=xml.nsmap)
        coords = linestring.find('coordinates', namespaces=xml.nsmap)

        self.name = doc.find('name', namespaces=xml.nsmap).text

        prev = Coordinate(0, 0) # dummy coordinate to keep mypy happy

        for i,group in enumerate(coords.text.split()): # split at white space

            # TODO: change how the exception is handled
            try:
                longitude, latitude, elevation = [float(x) for x in group.split(',')] # split into individual fields
            except:
                print(group)

            c = Coordinate(longitude, latitude)

            # the first point is always at distance 0 along the path
            if i == 0:
                self.points.append(PathPoint(0.0, c))
                prev = c
            else:
                d = distance_between_coords(prev, c)
                prev = c
                self.race_length += d
                self.points.append(PathPoint(self.race_length, c))


    def __repr__(self):

        if self.name is not None:
            return '<race: {}, race_length: {}>'.format(self.name, self.race_length)
        else:
            return '<race not initialized>'


# little demo program
# rp = RacePath()
# rp.load_path('paths/ASC_2020.kml')

# d = 0
# diff = 0
# while d < rp.race_length:
#     c = rp.get_point_from_distance(d)
#     x = rp.get_distance_from_point(c)
#     if abs(d-x) > diff:
#         diff = abs(d-x)
#     print(d, x, d-x)
#     d += 10 * 1000