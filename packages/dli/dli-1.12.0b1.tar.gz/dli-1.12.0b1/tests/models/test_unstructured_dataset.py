from unittest.mock import MagicMock

import pytest
from s3transfer.futures import TransferFuture

from dli.models.unstructured_dataset_model import UnstructuredDatasetModel
from dli.models.structured_dataset_model import StructuredDatasetModel


class TestUnstructuredDataset:

    def test_model_factory_instantiation(self, test_client, unstructured_dataset_request_index_v2):
        test_client._session.get.return_value.json.side_effect = [
            unstructured_dataset_request_index_v2,
        ]

        test_ds = test_client.datasets()
        assert type(test_ds.get("TestDataset")).__name__ == UnstructuredDatasetModel.__name__
        assert type(test_ds.get("OtherDataset")).__name__ == StructuredDatasetModel.__name__

    def test_list(self, monkeypatch, client, unstructured_object_summaries_s3):
        class MockResource:

            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.list()
        assert len(ls) == 10

    def test_list_method_with_structured_args(self, object_summaries_s3, monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        with pytest.raises(AttributeError) as e_info:
            ls = dataset.list(partitions=["document_id=1"])
        assert("EXISTS" in str(e_info.value.args[0]))

    def test_none_existing_method(self, object_summaries_s3, monkeypatch, client):

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        with pytest.raises(AttributeError) as e_info:
            ls = dataset.dask_dataframe()
        assert("EXISTS" not in str(e_info.value.args[0]))

    def test_download(self, unstructured_object_summaries_s3, monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.download("test")
        assert(len(ls) == 8)

    def test_download_method_with_structured_args(self, unstructured_object_summaries_s3, monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        with pytest.raises(AttributeError) as e_info:
            ls = dataset.download("test", flatten=True, partitions="document_id=1")
        assert("EXISTS" in str(e_info.value.args[0]))

    def test_download_filter_attachments(self, unstructured_object_summaries_s3, monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.download("test", with_attachments=False)
        assert all(map(lambda x: "attachment" not in x, ls))
        assert len(ls) == 6

    def test_download_filter_metadata(self, unstructured_object_summaries_s3, monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.download("test", with_metadata=False)
        assert all(map(lambda x: "metadata" not in x, ls))
        assert len(ls) == 6

    def test_download_filter_attachments_and_metadata(self, unstructured_object_summaries_s3, monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.download("test", with_attachments=False, with_metadata=False)
        assert all(map(lambda x: "attachment" not in x and "metadata" not in x, ls))
        assert len(ls) == 4

    def test_download_filter_only_documents(self, unstructured_object_summaries_s3, monkeypatch, client):

        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        # type exist list
        ls = dataset.download("test", with_attachments=False, with_metadata=False,
                              document_types=["xml"])
        assert all(map(lambda x: ".xml" in x, ls))

        # type exist
        ls = dataset.download("test", with_attachments=False, with_metadata=False,
                              document_types="xml")
        assert all(map(lambda x: ".xml" in x, ls))

        # mix type exist/not exist list
        ls = dataset.download("test", with_attachments=False, with_metadata=False,
                              document_types=["xml", "html"])
        assert all(map(lambda x: ".xml" in x, ls))

        # type not exist
        ls = dataset.download("test", with_attachments=False, with_metadata=False,
                              document_types="html")
        assert len(ls) == 0

        # type exist list 2
        ls = dataset.download("test", with_attachments=False, with_metadata=False,
                              document_types=["xml", "parquet"])
        assert all(map(lambda x: ".xml" in x or ".parquet" in x, ls))
        assert len(ls) == 4

    def test_download_skip_zero_document_folders(self, unstructured_object_summaries_s3,
                                                 monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        # there are only attachment and metadata in document_id=3
        ls = dataset.download("test", skip_folders_with_zero_matching_documents=True)
        assert all(map(lambda x: "document_id=3" not in x, ls))

        ls = dataset.download("test", skip_folders_with_zero_matching_documents=False)
        assert any(map(lambda x: "document_id=3" in x, ls))


    def test_download_metadata(self, unstructured_object_summaries_s3, monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        # there are only attachment and metadata in document_id=3
        ls = dataset.download_metadata("test")
        assert all(map(lambda x: "metadata" in x, ls))


    def test_download_attachments(self, unstructured_object_summaries_s3, monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        # there are only attachment and metadata in document_id=3
        ls = dataset.download_attachments("test")
        assert all(map(lambda x: "attachment" in x, ls))


    #check against dl-5214
