import traceback
from .models import City, Province, CityAdditionalInfo
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic as GD
import openrouteservice


class RoadDistance:
    def __init__(self):
        self.openrouteservice_api_key = "5b3ce3597851110001cf6248e67e0a0608cd4992ba3e9cc408523cff"

    @staticmethod
    def method_2(coords_1, coords_2):
        """
        :param coords_1:  (35.6892, 51.3890) tuple
        :param coords_2: (31.3200, 48.6700)  tuple
        :return:
        """
        try:
            return GD(coords_1, coords_2).km
        except (Exception, ):
            return 0

    def method_1(self, coords_1, coords_2):
        try:
            client = openrouteservice.Client(key=self.openrouteservice_api_key)
            res = client.directions((coords_1, coords_2))
            res = res['routes'][0]['summary']
            distance = res['distance'] / 1000
            right_distance = self.method_2(coords_1, coords_2)
            distance = (distance + right_distance) / 2
            return {
                "distance": distance,
                "duration": res['duration']
            }
        except (Exception, ):
            print(traceback.format_exc())
            return {
                "distance": 0,
                "duration": 0
            }

    def calculate_distance(self, *args):
        return self.method_1(*args)


class LocationProvider:
    def __init__(self, service=None, api_key=None):
        self.service = 'OpenCageGeocode' if not service else service
        self.api_key = "66cedbc483f04cc4a4972bcf6ddc1605" if not api_key else api_key
        self.location_instance = None
        self.str_parameters = False

    def save_city_info_in_model(self, city_id, province_id, country_id, city_data):
        """
        :param city_id:
        :param province_id:
        :param country_id:
        :param city_data: {
            "latitude", "longitude", "city_profile"
        }
        :return:
        """
        try:
            latitude, longitude, city_profile = 0, 0, ""
            if self.service == 'OpenCageGeocode':
                latitude, longitude = city_data['latitude'], city_data['longitude']
                city_profile = city_data.get('city_profile', '')

            new_city_info = CityAdditionalInfo(
                city_id=city_id,
                province_id=province_id,
                country_id=country_id,
                latitude=latitude,
                longitude=longitude,
                city_profile=city_profile
            )
            new_city_info.save()
        except (Exception, ):
            return

    def send_request_open_cage_geocode(self, city, province, country):
        """
        :param city: str name
        :param province: str name
        :param country: str name
        :return:
        """
        try:
            query = self.create_payload(city, province, country)
            result = self.location_instance.geocode(query)

            return {
                "city": city,
                "province": province,
                "country": country,
                "latitude": result[0]['geometry']['lat'],
                "longitude": result[0]['geometry']['lng'],
                "city_profile": result[0].get('formatted')
            }
        except (Exception, ):
            return

    def create_payload(self, *args, **kwargs):
        if self.service == 'OpenCageGeocode':
            create_query_open_cage_geocode = lambda x, y, z: f"{x}, {y}, {z}"  # x=city, y=province, z=country
            return create_query_open_cage_geocode(*args, **kwargs)

    def send_request(self, *args, **kwargs):
        if self.service == 'OpenCageGeocode':
            return self.send_request_open_cage_geocode(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.service == 'OpenCageGeocode':
            self.str_parameters = True
            self.location_instance = OpenCageGeocode(self.api_key)


class CityInfo(LocationProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_city_name(city_id):
        """
        :param city_id: pooke city id int
        :return: en name
        """
        try:
            city = City.objects.get(city_id=city_id)
            return city.name_en
        except (Exception, ):
            return

    @staticmethod
    def get_province_name(province_id):
        """
        :param province_id: pooke province id int
        :return: en name
        """
        try:
            province = Province.objects.get(province_id=province_id)
            return province.name_en
        except (Exception, ):
            return

    def get_city_info(self, city_id, country_id: int = 1):
        """
        :param city_id: int
        :param country_id: int (optional)
        :return: return info
        """
        try:
            city_info = CityAdditionalInfo.objects.filter(
                city_id=city_id
            ).first()

            if city_info:

                return {
                    "city": city_info.city.name_en,
                    "province": city_info.province.name_en,
                    # "country": country,
                    "latitude": city_info.latitude,
                    "longitude": city_info.longitude,
                }

            city = City.objects.filter(city_id=city_id).first()
            this_input = {}
            if self.str_parameters:
                # it means service get locations name not id
                # get name parameters
                country = 'Iran' if country_id == 1 else ""  # movaghat

                this_input.update({
                    "city": self.get_city_name(city_id),
                    "province": self.get_province_name(city.province_id),
                    "country": country
                })
            else:
                # add for other services
                pass

            city_info = self.send_request(**this_input)

            self.save_city_info_in_model(city_id, city.province_id, country_id, city_info)

            return city_info
        except (Exception, ):
            return


class RouteInfo:
    def __init__(self, origin, destination):
        self.origin_id = origin
        self.destination_id = destination

    @property
    def is_valid_input(self):
        try:
            # set content
            return True
        except (Exception, ):
            return

    def __getattr__(self, attribute_name):
        pre_check = [
            self.is_valid_input,
            hasattr(self, attribute_name)
        ]

        if all(pre_check):
            return getattr(self, attribute_name)

        return {
            "status": "failed",
            "msg": "Bad Request"
        }

    def get_coordinates(self):
        get_city_info_instance = CityInfo(service='OpenCageGeocode')
        get_city_info_instance()
        origin_info = get_city_info_instance.get_city_info(self.origin_id)
        destination_info = get_city_info_instance.get_city_info(self.destination_id)

        origin_cord = (origin_info['latitude'], origin_info['longitude'])
        destination_cord = (destination_info['latitude'], destination_info['longitude'])

        return origin_cord, destination_cord

    def get_route(self):
        origin_cord, destination_cord = self.get_coordinates()

        return RoadDistance().calculate_distance(origin_cord, destination_cord)
