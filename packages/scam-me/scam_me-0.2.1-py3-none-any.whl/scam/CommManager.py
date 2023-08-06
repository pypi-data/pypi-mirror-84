import requests
import json


class CommManager:

    def __init__(self):
        self.url = 'http://40.66.46.195:8000/'

    def get_destinations(self):
        """

        @return: json containing all possible destinations
        """
        res = requests.get(url=self.url + 'destinations')
        if res.status_code != 200:
            raise Exception('An error occurred')
        return res.json()

    def make_reservation(self, location: int, name: str, phone_number: str, persons: int, reservation: int):
        """

        @param location:
        @param name:
        @param phone_number:
        @param persons:
        @param reservation:
        @return: json containing reservation id on success, exception otherwise
        """
        data = {'location': location,
                'name': name,
                'phone_number': phone_number,
                'persons': persons,
                'reservation': reservation}

        res = requests.post(url=self.url + 'reservation', data=json.dumps(data))

        if res.status_code != 200:
            raise Exception('An error occurred')

        return res.json()

    def get_reservations(self, reservation_id=-1, name=''):
        """

        @param reservation_id
        @param name
        @return: json containing all reservation info on success, Exception otherwise
        """
        if reservation_id == -1:
            res = requests.get(url=self.url + 'reservations/{}'.format(name))
        else:
            res = requests.get(url=self.url + 'reservation/{}'.format(reservation_id))

        if res.status_code == 404:
            raise Exception('Reservation not found')

        if res.status_code != 200:
            raise Exception('An error occurred')

        return res.json()

    def delete_reservation(self, reservation_id: int):
        """

        @param reservation_id
        @return: True on success, Exception otherwise
        """
        try:
            res = requests.delete(url=self.url + 'reservation/{}'.format(reservation_id))
        except Exception:
            raise Exception('Reservation not found')

        if res.status_code != 200:
            raise Exception('An error occurred')

        return True

    def modify_reservation(self,
                           reservation_id: int,
                           location: int,
                           name: str,
                           phone_number: str,
                           persons: int,
                           reservation: int):
        """

        @param reservation_id
        @param location
        @param name
        @param phone_number
        @param persons
        @param reservation
        @return: True on success, Exception otherwise
        """
        data = {'location': location,
                'name': name,
                'phone_number': phone_number,
                'persons': persons,
                'reservation': reservation}

        try:
            res = requests.put(url=self.url + 'reservation/{}'.format(reservation_id), data=json.dumps(data))
        except Exception:
            raise Exception('Reservation not found')

        if res.status_code != 200:
            raise Exception('An error occurred')

        return True
