"""DarkRunApiTest class"""

import unittest

from metadata_client import MetadataClient
from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *


class DarkRunApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL)

    def test_create_dark_run_api(self):
        __unique_name = Generators.generate_unique_name('DarkRunApi')
        __unique_identifier = Generators.generate_unique_identifier()
        dark_run = {
            'dark_run': {
                'proposal_id': -1,
                'detector_id': -2,
                'detector_identifier': 'TEST_DET_CI-2',
                'detector_type_id': -1,
                'pdu_physical_names':
                    '["PDU-3_DO_NOT_DELETE", "PDU-2_DO_NOT_DELETE"]',
                'runs_info': str([1]),
                'operation_mode_id': -2,
                'operation_mode_identifier': 'OPERATION_MODE-2_DO_NOT_DELETE',
                'operation_mode_name': 'OPERATION_MODE-2_DO_NOT_DELETE',
                'flg_status': 'R',
                'pdu_karabo_das': '',
                'size': '2,5Gb',
                'calcat_url': 'https://www.new_example.com:123#calcat',
                'globus_url': 'https://www.new_example.com:123#globus',
                'input_path': '/this/is/input/path',
                'output_path': '/this/is/output/path',
                'calcat_feedback': 'This dark run performed with success!',
                'description': 'desc 01'
            }
        }

        expect = dark_run['dark_run']

        #
        # Create new entry (should succeed)
        #
        received = self.__create_entry_api(dark_run, expect)

        dark_run_id = received['id']
        dark_run_proposal_id = received['proposal_id']

        #
        # Get entry by proposal_id
        #
        self.__get_all_entries_by_proposal_id_api(dark_run_proposal_id, expect)

        #
        # Get entry by ID
        #
        self.__get_entry_by_id_api(dark_run_id, expect)

        #
        # Put entry information (update some fields should succeed)
        #
        self.__update_entry_api(dark_run_id, expect)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        self.__delete_entry_by_id_api(dark_run_id)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'proposal_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_type_id', STRING)
        self.assert_eq_hfield(receive, expect, 'pdu_physical_names', STRING)
        self.assert_eq_hfield(receive, expect, 'runs_info', STRING),
        self.assert_eq_hfield(receive, expect, 'operation_mode_id', STRING),
        self.assert_eq_hfield(receive, expect, 'operation_mode_name', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_status', STRING)
        self.assert_eq_hfield(receive, expect, 'pdu_karabo_das', STRING)
        self.assert_eq_hfield(receive, expect,
                              'operation_mode_identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'size', STRING)
        self.assert_eq_hfield(receive, expect, 'calcat_url', STRING)
        self.assert_eq_hfield(receive, expect, 'globus_url', STRING)
        self.assert_eq_hfield(receive, expect, 'input_path', STRING)
        self.assert_eq_hfield(receive, expect, 'output_path', STRING)
        self.assert_eq_hfield(receive, expect, 'calcat_feedback', STRING)
        self.assert_eq_hfield(receive, expect, 'description', STRING)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_dark_run_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = Generators.generate_unique_name('ExpTypeApiUpd')
        unique_id_upd = Generators.generate_unique_identifier(1)
        dark_run_upd = {
            'dark_run': {
                # Not changed fields!
                'proposal_id': -1,
                'detector_id': -2,
                'detector_identifier': 'TEST_DET_CI-2',
                'detector_type_id': -1,
                'pdu_physical_names':
                    '["PDU-3_DO_NOT_DELETE", "PDU-2_DO_NOT_DELETE"]',
                'runs_info': str([1]),
                'operation_mode_id': -2,
                'operation_mode_identifier': 'OPERATION_MODE-2_DO_NOT_DELETE',
                'operation_mode_name': 'OPERATION_MODE-2_DO_NOT_DELETE',
                'pdu_karabo_das': '',

                # UPDATED FIELDS!
                'flg_status': 'F',
                'size': '1,5Gb',
                'calcat_url': 'https://www.new_example.com:123#calcat_UPDATED',
                'globus_url': 'https://www.new_example.com:123#globus_UPDATED',
                'input_path': '/this/is/input/path/UPDATED',
                'output_path': '/this/is/output/path/UPDATED',
                'calcat_feedback': 'This dark run performed with success UPD!',
                'description': 'desc 01 UPDATED!!!'
            }
        }

        response = self.client_api.update_dark_run_api(
            entry_id,
            dark_run_upd
        )

        resp_content = self.load_response_content(response)

        receive = resp_content
        expect_upd = dark_run_upd['dark_run']

        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(response.status_code, OK)

        # Not Changed fields
        self.assert_eq_hfield(receive, expect, 'proposal_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_type_id', STRING)
        self.assert_eq_hfield(receive, expect, 'pdu_physical_names', STRING)
        self.assert_eq_hfield(receive, expect, 'runs_info', STRING)
        self.assert_eq_hfield(receive, expect, 'operation_mode_id', STRING)
        self.assert_eq_hfield(receive, expect, 'operation_mode_name', STRING)
        self.assert_eq_hfield(receive, expect, 'pdu_karabo_das', STRING)
        self.assert_eq_hfield(receive, expect,
                              'operation_mode_identifier', STRING)

        # Updated fields
        field = 'flg_status'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'size'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'calcat_url'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'globus_url'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'input_path'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'output_path'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'calcat_feedback'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_proposal_id_api(self, proposal_id, expect):
        response = self.client_api.get_all_dark_runs_by_proposal_id_api(
            proposal_id)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_dark_run_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_dark_run_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()
