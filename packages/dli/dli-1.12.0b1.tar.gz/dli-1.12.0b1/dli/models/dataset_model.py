#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import os
import uuid
import warnings
from abc import ABCMeta
from typing import List, Optional, Callable, Tuple

import s3transfer
from tqdm import tqdm


from s3transfer.manager import TransferManager, TransferConfig
import boto3.s3.transfer as s3transfer

from dli.aws import create_refreshing_session, trace_logger
from dli.client import utils
from dli.models import AttributesDict
from dli.models.file_model import get_or_create_os_path


class DatasetModel(AttributesDict, metaclass=ABCMeta):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, )

    def __endpoint_url(self):
        return f'https://{self._client._environment.s3_proxy}'

    def _check_access(self):
        if not self.has_access:
            raise Exception(
                'Unfortunately the user you are using '
                'does not have access to this dataset. '
                'Please request access to the package/dataset '
                "to be able to retrieve this content."
            )

    @staticmethod
    def _get_transfer_manager(s3_client, config):
        return TransferManager(s3_client, config=config)

    @property
    def id(self):
        return self.dataset_id

    def __list(
        self,
        request_id=None,
        custom_filter_func: Callable[[List[Tuple[str, int]]], List[Tuple[str, int]]] = None,
        filter_path: Optional[str] = None,
        absolute_path: bool = True,
        skip_hidden_files: bool = True,
    ) -> List[str]:
        """
        List all the paths to files in the dataset. Calls go via the
        Datalake's S3 proxy, so the returned paths will be returned in the
        style of the S3 proxy, so in the pattern
        `s3://organisation_short_code/dataset_short_code/<path>`.
        S3 proxy does not return direct paths to the real location on S3 as
        they may be sensitive.

        The list will filter out paths where:
        * The size is zero bytes.
        * The name of any partition within the path is prefixed with a `.` or
        a `_` as that means it is intended as a hidden file.
        * The name of any partition within the path is exactly the word
        `metadata`.
        * It is a directory rather than a file.
        * Files with the wrong extension for the dataset's type i.e for
        a .parquet dataset we will return only .parquet files, zero .csv
        files.

        This list will filter based on `load_type` of the dataset. When the
        dataset's `load_type` is `Incremental Load` then files will be listed
        from all of the `as_of_date` partitions on S3. When the
        dataset's `load_type` is `Full Load` then files will be listed only
        the most recent `as_of_date` partition on S3.
        Please see the support library documentation for more information
        about how the `load type` affects the data you can access in a dataset:
        https://supportlibrary.ihsmarkit.com/display/DLSL/Exploring+Datasets#ExploringDatasets-Howthe%60loadtype%60affectsthedatayoucanaccessinadataset

        Parameters
        ----------
        :param str request_id: Optional. Automatically generated value
            used by our logs to correlate a user journey across several
            requests and across multiple services.

        :param custom_filter_func: A function which may optionally filter the s3 paths returned during the first
        stage of download (namely path lookup as part of list is filtered).

        :param str filter_path: Optional. If provided only a subpath matching
            the filter_path will be matched. This is less flexible than using
            the `partitions` parameter, so we recommend you pass in
            `partitions` instead. The `partitions` can deal with the
            partitions in the path being in any order, but filter_path relies
            on a fixed order of partitions that the user needs to know ahead
            of time.

            Example usage to get all paths that start with the `as_of_date`
            2020. Note this is a string comparison, not a datetime comparison.

            .. code-block:: python

                dataset.list(filter_path='as_of_date=2020')

        :param bool absolute_path: True (default) for returning an
            absolute path to the path on the S3 proxy. False to return a
            relative path (this is useful if using a TransferManager).

        :param bool skip_hidden_files: True (default) skips files that have
            been uploaded to S3 by Spark jobs. These usually start with a
            `.` or `_`.
        """

        files = self.__list_with_size(
            request_id=request_id,
            custom_filter_func=custom_filter_func,
            filter_path=filter_path,
            absolute_path=absolute_path,
            skip_hidden_files=skip_hidden_files
        )
        # this could be a completely empty prefix.
        if files:
            paths, _ = zip(*files)
        else:
            return []

        return list(paths)

    def __list_with_size(
        self,
        request_id=None,
        custom_filter_func: Callable[[List[Tuple[str, int]]], List[Tuple[str, int]]] = None,
        filter_path: Optional[str] = None,
        absolute_path: bool = True,
        skip_hidden_files: bool = True,
    ) -> List[Tuple[str, int]]:
        """
        List all the paths to files in the dataset. Calls go via the
        Datalake's S3 proxy, so the returned paths will be returned in the
        style of the S3 proxy, so in the pattern
        `s3://organisation_short_code/dataset_short_code/<path>`.
        S3 proxy does not return direct paths to the real location on S3 as
        they may be sensitive.

        The list will filter out paths where:
        * The size is zero bytes.
        * The name of any partition within the path is prefixed with a `.` or
        a `_` as that means it is intended as a hidden file.
        * The name of any partition within the path is exactly the word
        `metadata`.
        * It is a directory rather than a file.
        * Files with the wrong extension for the dataset's type i.e for
        a .parquet dataset we will return only .parquet files, zero .csv
        files.

        This list will filter based on `load_type` of the dataset. When the
        dataset's `load_type` is `Incremental Load` then files will be listed
        from all of the `as_of_date` partitions on S3. When the
        dataset's `load_type` is `Full Load` then files will be listed only
        the most recent `as_of_date` partition on S3.
        Please see the support library documentation for more information
        about how the `load type` affects the data you can access in a dataset:
        https://supportlibrary.ihsmarkit.com/display/DLSL/Exploring+Datasets#ExploringDatasets-Howthe%60loadtype%60affectsthedatayoucanaccessinadataset

        Parameters
        ----------
        :param str request_id: Optional. Automatically generated value
            used by our logs to correlate a user journey across several
            requests and across multiple services.

        :param custom_filter_func: A function which may optionally filter the
        s3 paths returned during the first stage of download (namely path
        lookup as part of list is filtered).

        :param str filter_path: Optional. If provided only a subpath matching
            the filter_path will be matched. This is less flexible than using
            the `partitions` parameter, so we recommend you pass in
            `partitions` instead. The `partitions` can deal with the
            partitions in the path being in any order, but filter_path relies
            on a fixed order of partitions that the user needs to know ahead
            of time.

            Example usage to get all paths that start with the `as_of_date`
            2020. Note this is a string comparison, not a datetime comparison.

            .. code-block:: python

                dataset.list(filter_path='as_of_date=2020')

        :param bool absolute_path: True (default) for returning an
            absolute path to the path on the S3 proxy. False to return a
            relative path (this is useful if using a TransferManager).

        :param bool skip_hidden_files: True (default) skips files that have
            been uploaded to S3 by Spark jobs. These usually start with a
            `.` or `_`.
        """

        self._check_access()

        if request_id is None:
            request_id = str(uuid.uuid4())

        trace_logger.info(
            f"The following GET Requests to '{self.__endpoint_url()}' "
            f"will be using request_id: '{request_id}'"
        )

        def add_request_id_to_session(**kwargs):
            kwargs["request"].headers['X-Request-ID'] = request_id

        session = create_refreshing_session(
            dli_client_session=self._client.session,
            event_hooks=add_request_id_to_session
        )
        s3_resource = session.resource(
            's3',
            endpoint_url=self.__endpoint_url()
        )

        bucket = s3_resource.Bucket(
            self.organisation_short_code
        )

        filter_prefix = self.short_code + (
            '' if self.short_code.endswith('/') else '/'
        )

        if filter_path:
            filter_prefix = filter_prefix + filter_path.lstrip('/')

        def _to_s3_proxy_path_and_size(object_summary) -> (str, int):
            if absolute_path:
                return (f"s3://{self.organisation_short_code}/" \
                       f"{object_summary.key}", object_summary.size)
            else:
                return (object_summary.key, object_summary.size)

        # Convert each object_summary into an S3 proxy path.
        object_summaries = [
            object_summary for object_summary in bucket.objects.filter(
                # Prefix searches for exact matches and folders
                Prefix=filter_prefix
            )
        ]

        self._client.logger.info(
            "Number of paths on S3 for this dataset: "
            f"'{len(object_summaries)}'"
        )

        # Convert each object_summary into an S3 proxy path.
        paths: List[Tuple[str, int]] = [
            _to_s3_proxy_path_and_size(object_summary) for object_summary in
            object_summaries if not object_summary.key.endswith('/')
        ]

        self._client.logger.info(
            "Number of paths on S3 for this dataset "
            f"after filtering out empty directories: '{len(paths)}'"
        )

        if skip_hidden_files:
            # [DL-4545][DL-4536][DL-5209] Do not read into files or
            # directories that are cruft from Spark which Spark will ignore
            # on read, e.g. files/dirs starting with `.` or `_` are hidden
            # to Spark.

            # Skip as_of_date=latest as it is a Spark temporary folder.

            def is_hidden_file(path: str):
                return (
                        path.startswith('.') or
                        path.startswith('_') or
                        (
                            path == 'metadata' and
                            self.content_type != "Unstructured"
                        ) or
                        path == 'as_of_date=latest'
                )

            paths: List[Tuple[str, int]] = [
                path for path in paths
                if not any(is_hidden_file(split) for split in path[0].split('/'))
            ]

            self._client.logger.info(
                f"Number of paths on S3 for this dataset "
                f"after filtering out hidden files: '{len(paths)}'"
            )

        if custom_filter_func:
            len_before = len(paths)
            self._client.logger.info(
                f'Filtering {len_before} paths according to '
                f'{custom_filter_func} logic.'
            )

            paths = custom_filter_func(paths=paths)
            self._client.logger.info(
                f'Filtered out {len_before - len(paths)} / {len_before} paths '
                f'according to constraints.'
            )

            if len(paths) == 0:
                self._client.logger.warning(
                    f'There are no items matching your filter settings. Check '
                    f'your filter settings.\n'
                )
                return []

        return paths

    def __download(
        self,
        destination_path: str,
        flatten: Optional[bool] = False,
        filter_path: Optional[str] = None,
        custom_filter_func: Callable[[List[str]], List[str]] = None,
        skip_hidden_files: Optional[bool] = True
    ) -> List[str]:
        """
        Equivalent to the exposed `download` method. Used as a base for
        all models

        Additional Parameters
        ----------
        :param custom_filter_func: A function which may optionally filter
        the s3 paths returned during the first stage of download (namely
        path lookup as part of list is filtered).
        """

        self._check_access()
        request_id = str(uuid.uuid4())

        files = self.__list_with_size(
            request_id=request_id,
            custom_filter_func=custom_filter_func,
            filter_path=filter_path,
            absolute_path=False,  # TransferManager uses relative paths.
            skip_hidden_files=skip_hidden_files,
        )

        if files:
            paths, sizes = zip(*files)
        else:
            return []

        def __add_request_id_to_session(**kwargs):
            kwargs["request"].headers['X-Request-ID'] = request_id

        s3_resource = create_refreshing_session(
            dli_client_session=self._client.session,
            event_hooks=__add_request_id_to_session
        ).resource(
            's3',
            endpoint_url=self.__endpoint_url()
        )

        s3_client = s3_resource.meta.client

        # multipart_threshold -- The transfer size threshold for which
        # multipart uploads, downloads, and copies will automatically
        # be triggered.
        # 500 GB should be a large enough number so that the download never
        # triggers multipart download on cloudfront.
        KB = 1024
        GB = KB * KB * KB
        multipart_threshold = 500 * GB

        progress = tqdm(
            desc='Downloading ',
            total=sum(sizes), unit='B', unit_scale=1,
            position=0,
        )

        config = TransferConfig(
            multipart_threshold=multipart_threshold,
        )

        transfer_manager_context = DatasetModel._get_transfer_manager(
            s3_client,
            config
        )

        with transfer_manager_context as transfer_manager:
            with progress as pbar:
                _paths_and_futures = []

                for path in paths:
                    if not path.endswith('/'):
                        to_path = get_or_create_os_path(
                            s3_path=path,
                            to=destination_path,
                            flatten=flatten
                        )

                        self._client.logger.info(
                            f'Downloading {path} to: {to_path}...'
                        )

                        if os.path.exists(to_path):
                            warnings.warn(
                                'File already exists. Overwriting.'
                            )

                        # returns a future
                        future = transfer_manager.download(
                            self.organisation_short_code,
                            path,
                            to_path,
                            subscribers=[s3transfer.ProgressCallbackInvoker(pbar.update)]
                        )

                        _paths_and_futures.append((to_path, future))

                _successful_paths = []
                for path, future in _paths_and_futures:
                    try:
                        # This will block for this future to complete,
                        # but other futures will keep running in the
                        # background.
                        future.result()
                        _successful_paths.append(path)
                    except Exception as e:
                        message = f'Problem while downloading:' \
                                  f'\nfile path: {path}' \
                                  f'\nError message: {e}\n\n'

                        self._client.logger.error(message)
                        print(message)

                return _successful_paths

    def metadata(self):
        """
        Once you have selected a dataset, you can print the metadata (the
        available fields and values).

        :example:

            .. code-block:: python
                # Get all datasets.
                >>> datasets = client.datasets()

                # Get metadata of the 'ExampleDatasetShortCode' dataset.
                >>> datasets['ExampleDatasetShortCode'].metadata()

        :example:

            .. code-block:: python
                # Get an exact dataset using the dataset_short_code and
                # organisation_short_code.
                >>> dataset = client.get_dataset(dataset_short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                # Get metadata of the dataset.
                >>> dataset.metadata()

        :example:

            .. code-block:: python
                # Get all datasets.
                >>> dataset = client.datasets()['ExampleDatasetShortCode']
                # Get metadata of the dataset.
                >>> dataset.metadata()

        :return: Prints the metadata.
        """
        utils.print_model_metadata(self)
