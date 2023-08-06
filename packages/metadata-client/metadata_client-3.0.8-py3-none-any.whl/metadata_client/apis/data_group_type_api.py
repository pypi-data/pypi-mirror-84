"""DataGroupTypeApi module class"""

import json

from ..common.base import Base


class DataGroupTypeApi(Base):
    def create_data_group_type_api(self, data_group_type):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(data_group_type))

    def delete_data_group_type_api(self, data_group_type_id):
        api_url = self.__get_api_url(data_group_type_id)
        return self.api_delete(api_url)

    def update_data_group_type_api(self, data_group_type_id, data_group_type):
        api_url = self.__get_api_url(data_group_type_id)
        return self.api_put(api_url, data=json.dumps(data_group_type))

    def get_data_group_type_by_id_api(self, data_group_type_id):
        api_url = self.__get_api_url(data_group_type_id)
        return self.api_get(api_url, params={})

    def get_all_data_group_types_by_name_api(self, name):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name})

    def get_all_data_group_types_api(self):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'data_group_types/'
        return self.get_api_url(model_name, api_specifics)
