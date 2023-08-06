from base_client import BaseClient


class DriverClient(BaseClient):
    def add_driver(self, first_name=None, last_name=None, id_type=None, id_number=None, gender=None, email=None,
                   phone=None, date_of_birth=None, license_number=None):
        return self.post('driver', first_name=first_name, last_name=last_name, id_type=id_type, id_number=id_number,
                         gender=gender, email=email, phone=phone, date_of_birth=date_of_birth, license_number=license_number)

    def get_driver(self, driver_id):
        return self.get('driver/{}'.format(driver_id))



