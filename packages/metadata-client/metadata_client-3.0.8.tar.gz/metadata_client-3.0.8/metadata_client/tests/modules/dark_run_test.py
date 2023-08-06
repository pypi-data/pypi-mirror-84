"""DarkRunTest class"""

import unittest

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.secrets import *
from ...modules.dark_run import DarkRun

MODULE_NAME = DARK_RUN


class DarkRunTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        self.mdc_client = MetadataClient(
            client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
            client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
            token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
            refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
            auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
            scope=CLIENT_OAUTH2_INFO['SCOPE'],
            user_email=CLIENT_OAUTH2_INFO['EMAIL'],
            base_api_url=BASE_API_URL
        )

        self.dark_1 = {
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

        self.dark_01_upd = {
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

    def test_create_dark_run(self):
        repo_01 = DarkRun(
            metadata_client=self.mdc_client,
            proposal_id=self.dark_1['proposal_id'],
            detector_id=self.dark_1['detector_id'],
            detector_identifier=self.dark_1['detector_identifier'],
            detector_type_id=self.dark_1['detector_type_id'],
            pdu_physical_names=self.dark_1['pdu_physical_names'],
            runs_info=self.dark_1['runs_info'],
            operation_mode_id=self.dark_1['operation_mode_id'],
            operation_mode_identifier=self.dark_1['operation_mode_identifier'],
            operation_mode_name=self.dark_1['operation_mode_name'],
            flg_status=self.dark_1['flg_status'],
            pdu_karabo_das=self.dark_1['pdu_karabo_das'],
            size=self.dark_1['size'],
            calcat_url=self.dark_1['calcat_url'],
            globus_url=self.dark_1['globus_url'],
            input_path=self.dark_1['input_path'],
            output_path=self.dark_1['output_path'],
            calcat_feedback=self.dark_1['calcat_feedback'],
            description=self.dark_1['description'])

        #
        # Create new entry (should succeed)
        #
        result1 = repo_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.dark_1)

        dark_run = result1['data']
        dark_run_id = result1['data']['id']
        dark_run_proposal_id = result1['data']['proposal_id']

        #
        # Get entry by proposal_id
        #
        res3 = DarkRun.get_all_dark_runs_by_proposal_id(self.mdc_client,
                                                        dark_run_proposal_id)

        self.assertEqual(res3['success'], True)
        self.assertEqual(res3['info'], 'Got dark_run successfully')
        self.assertIn('\'proposal_id\': -1', str(res3['data']))
        self.assertIn('\'operation_mode_id\': -2', str(res3['data']))
        self.assertIn('\'detector_id\': -2', str(res3['data']))

        #
        # Get entry by ID
        #
        result4 = DarkRun.get_by_id(self.mdc_client, dark_run_id)
        self.assert_find_success(MODULE_NAME, result4, self.dark_1)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result5 = DarkRun.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        repo_01.proposal_id = self.dark_01_upd['proposal_id']
        repo_01.detector_id = self.dark_01_upd['detector_id']
        repo_01.detector_identifier = self.dark_01_upd['detector_identifier']
        repo_01.detector_type_id = self.dark_01_upd['detector_type_id']
        repo_01.pdu_physical_names = self.dark_01_upd['pdu_physical_names']
        repo_01.runs_info = self.dark_01_upd['runs_info']
        repo_01.operation_mode_id = self.dark_01_upd['operation_mode_id']
        repo_01.operation_mode_identifier = self.dark_01_upd[
            'operation_mode_identifier']
        repo_01.operation_mode_name = self.dark_01_upd['operation_mode_name']
        repo_01.flg_status = self.dark_01_upd['flg_status']
        repo_01.pdu_karabo_das = self.dark_01_upd['pdu_karabo_das']
        repo_01.size = self.dark_01_upd['size']
        repo_01.calcat_url = self.dark_01_upd['calcat_url']
        repo_01.globus_url = self.dark_01_upd['globus_url']
        repo_01.input_path = self.dark_01_upd['input_path']
        repo_01.output_path = self.dark_01_upd['output_path']
        repo_01.calcat_feedback = self.dark_01_upd['calcat_feedback']
        repo_01.description = self.dark_01_upd['description']
        result6 = repo_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.dark_01_upd)

        #
        # Put entry information (update some fields should throw an error)
        #
        repo_01.globus_url = '#' * 251  # String with length of 251
        repo_01.description = self.dark_01_upd['description']
        result7 = repo_01.update()
        expect_app_info = {
            'globus_url': ['URL length allows only 250 characters']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = repo_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = repo_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

        #
        # fields_validation
        #

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'proposal_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_type_id', STRING)
        self.assert_eq_hfield(receive, expect, 'pdu_physical_names', STRING)
        self.assert_eq_hfield(receive, expect, 'runs_info', STRING)
        self.assert_eq_hfield(receive, expect, 'operation_mode_id', STRING)
        self.assert_eq_hfield(receive, expect, 'operation_mode_identifier',
                              STRING)
        self.assert_eq_hfield(receive, expect, 'operation_mode_name', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_status', STRING)
        self.assert_eq_hfield(receive, expect, 'pdu_karabo_das', STRING)
        self.assert_eq_hfield(receive, expect, 'size', STRING)
        self.assert_eq_hfield(receive, expect, 'calcat_url', STRING)
        self.assert_eq_hfield(receive, expect, 'globus_url', STRING)
        self.assert_eq_hfield(receive, expect, 'input_path', STRING)
        self.assert_eq_hfield(receive, expect, 'output_path', STRING)
        self.assert_eq_hfield(receive, expect, 'calcat_feedback', STRING)
        self.assert_eq_hfield(receive, expect, 'description', STRING)


if __name__ == '__main__':
    unittest.main()
