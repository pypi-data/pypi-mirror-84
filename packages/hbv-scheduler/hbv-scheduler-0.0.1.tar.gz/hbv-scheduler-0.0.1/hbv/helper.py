from geopy.distance import geodesic


class Helper:
    @staticmethod
    def calc_time(point_a, point_b, appt_time=10, buffer=0):
        distance = round(geodesic(point_a, point_b).miles)
        # Assuming each mile takes only 6 mins
        return distance * 6 + buffer + appt_time
