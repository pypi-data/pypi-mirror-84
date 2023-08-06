"""ExperimentTypeApi module class"""

import json

from ..common.base import Base


class ExperimentTypeApi(Base):
    def create_experiment_type_api(self, experiment_type):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(experiment_type))

    def delete_experiment_type_api(self, experiment_type_id):
        api_url = self.__get_api_url(experiment_type_id)
        return self.api_delete(api_url)

    def update_experiment_type_api(self, experiment_type_id, experiment_type):
        api_url = self.__get_api_url(experiment_type_id)
        return self.api_put(api_url, data=json.dumps(experiment_type))

    def get_experiment_type_by_id_api(self, experiment_type_id):
        api_url = self.__get_api_url(experiment_type_id)
        return self.api_get(api_url, params={})

    def get_all_experiment_types_by_name_api(self, name):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'experiment_types/'
        return self.get_api_url(model_name, api_specifics)
