import os
from multiprocessing import Process, Value, Queue
from os.path import basename
from time import sleep
from typing import List
from time import time

import jsonpickle
from .connection import ServerConnection
from .resultservice import ResultService

from ..interfaces import EpochTrainResult, SystemStats, JobInfo
from .systemstats import SystemMonitor

import logging

logger = logging.getLogger(__name__)


class AydaCallback:
    def __init__(self):
        self.validation_data = None
        self.model = None

    def _implements_train_batch_hooks(self):
        """Determines if this Callback should be called for each train batch."""
        return True

    def _implements_test_batch_hooks(self):
        """Determines if this Callback should be called for each test batch."""
        return True

    def _implements_predict_batch_hooks(self):
        """Determines if this Callback should be called for each predict batch."""
        return False

    def set_params(self, params):
        self.params = params

    def set_model(self, model):
        self.model = model

    def on_batch_begin(self, batch, logs=None):
        """A backwards compatibility alias for `on_train_batch_begin`."""

    def on_batch_end(self, batch, logs=None):
        """A backwards compatibility alias for `on_train_batch_end`."""

    def on_epoch_begin(self, epoch, logs=None):
        """Called at the start of an epoch.

        Subclasses should override for any actions to run. This function should only
        be called during train mode.

        # Arguments
            epoch: integer, index of epoch.
            logs: dict, currently no data is passed to this argument for this method
                but that may change in the future.
        """

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch.

        Subclasses should override for any actions to run. This function should only
        be called during train mode.

        # Arguments
            epoch: integer, index of epoch.
            logs: dict, metric results for this training epoch, and for the
                validation epoch if validation is performed. Validation result keys
                are prefixed with `val_`.
        """

    def on_train_batch_begin(self, batch, logs=None):
        """Called at the beginning of a training batch in `fit` methods.

        Subclasses should override for any actions to run.

        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dict, has keys `batch` and `size` representing the current
                batch number and the size of the batch.
        """
        # For backwards compatibility
        self.on_batch_begin(batch, logs=logs)

    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of a training batch in `fit` methods.

        Subclasses should override for any actions to run.

        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dict, metric results for this batch.
        """
        # For backwards compatibility
        self.on_batch_end(batch, logs=logs)

    def on_test_batch_begin(self, batch, logs=None):
        """Called at the beginning of a batch in `evaluate` methods.

        Also called at the beginning of a validation batch in the `fit` methods,
        if validation data is provided.

        Subclasses should override for any actions to run.

        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dict, has keys `batch` and `size` representing the current
                batch number and the size of the batch.
        """

    def on_test_batch_end(self, batch, logs=None):
        """Called at the end of a batch in `evaluate` methods.

        Also called at the end of a validation batch in the `fit` methods,
        if validation data is provided.

        Subclasses should override for any actions to run.

        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dict, metric results for this batch.
        """

    def on_predict_batch_begin(self, batch, logs=None):
        """Called at the beginning of a batch in `predict` methods.

        Subclasses should override for any actions to run.

        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dict, has keys `batch` and `size` representing the current
                batch number and the size of the batch.
        """

    def on_predict_batch_end(self, batch, logs=None):
        """Called at the end of a batch in `predict` methods.

        Subclasses should override for any actions to run.

        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dict, metric results for this batch.
        """

    def on_train_begin(self, logs=None):
        """Called at the beginning of training.

        Subclasses should override for any actions to run.

        # Arguments
            logs: dict, currently no data is passed to this argument for this method
                but that may change in the future.
        """

    def on_train_end(self, logs=None):
        """Called at the end of training.

        Subclasses should override for any actions to run.

        # Arguments
            logs: dict, currently no data is passed to this argument for this method
                but that may change in the future.
        """

    def on_test_begin(self, logs=None):
        """Called at the beginning of evaluation or validation.

        Subclasses should override for any actions to run.

        # Arguments
            logs: dict, currently no data is passed to this argument for this method
                but that may change in the future.
        """

    def on_test_end(self, logs=None):
        """Called at the end of evaluation or validation.

        Subclasses should override for any actions to run.

        # Arguments
            logs: dict, currently no data is passed to this argument for this method
                but that may change in the future.
        """

    def on_predict_begin(self, logs=None):
        """Called at the beginning of prediction.

        Subclasses should override for any actions to run.

        # Arguments
            logs: dict, currently no data is passed to this argument for this method
                but that may change in the future.
        """

    def on_predict_end(self, logs=None):
        """Called at the end of prediction.

        Subclasses should override for any actions to run.

        # Arguments
            logs: dict, currently no data is passed to this argument for this method
                but that may change in the future.
        """


class MetricSender(AydaCallback):
    """
    Class for sending the metrics to a REST service using basic auth.
    It is implemented as Keras Callback but could also
    be used with other frameworks by calling the on_train_begin,
    on_epoch_end and on_train_end functions
    """

    def __init__(self, connection: ServerConnection, job_ref: str):
        """
        Args:
            job_ref: Job id to identify to which job the data belongs to
        """
        self.connection = connection
        self.metric_queue = Queue()
        self.stopped = Value("b", False)
        self.upload_process = Process()
        self.job_ref = job_ref
        super().__init__()

    def _upload_loop(self):
        self.stopped.value = False
        while not self.stopped.value:
            result = self.metric_queue.get()
            if not result:
                continue
            logger.info("Grab and send new Results")
            result_to_send = map_log_dict_to_epochresult(
                self.job_ref, result["epoch"], result["metrics"]
            )
            try:
                self.connection.send_server_request(
                    "send_train_results", {"result": jsonpickle.encode(result_to_send)}
                )
                logger.info("Upload metric successfull")
            except ConnectionError:
                logger.warning("Failed to upload metrics")
            sleep(5)

    def on_train_begin(self, _: dict = None):
        logger.info("start train")
        self.upload_process = Process(target=self._upload_loop)
        self.upload_process.start()

    def on_epoch_end(self, epoch: int, logs: dict = None):
        """
        Pushes the logs to the REST service.

        Args:
            epoch: The actual epoch
            logs: The metrics as dictionary. validation metrics should start with val_"

        """
        logger.info("epoch end")
        self.metric_queue.put({"metrics": logs, "epoch": epoch})

    def on_train_end(self, _: dict = None):
        self.stopped.value = True
        self.metric_queue.put(None)
        logger.info("MetricSender finalize")
        if self.upload_process.is_alive():
            self.upload_process.join()
        logger.info("MetricSender finish")


class SystemMonitorSender(AydaCallback):
    def __init__(self, connection: ServerConnection, job: JobInfo):
        self.connection = connection
        self.system_monitor = SystemMonitor()
        self.running = Value("b", False)
        self.epoch_size = job.train_options.epoch_size
        self.epochs = job.train_options.epochs
        self.job = job
        self.batch_finished = Queue()
        self.epoch_measurement = []
        self.process = Process(target=self.stat_loop)
        super().__init__()

    def on_train_begin(self, logs=None):
        self.process = Process(target=self.stat_loop)
        self.running.value = True
        self.process.start()

    def on_batch_begin(self, batch, logs=None):
        self.batch_finished.put(["batch", time()])

    def on_epoch_begin(self, epoch, logs=None):
        self.batch_finished.put(["epoch", time()])

    def on_train_end(self, logs=None):
        self.running.value = False
        self.batch_finished.put(["batch", time()])
        logger.info("SystemMonitorSender finalize")
        if self.process.is_alive():
            self.process.join()
        logger.info("SystemMonitorSender finished")

    def get_queued_data(self):
        while not self.batch_finished.empty():
            data = self.batch_finished.get()
            if data[0] == "batch":
                self.epoch_measurement[-1].append(data[1])
            else:
                self.epoch_measurement.append([])

        return self.epoch_measurement

    def get_stats(self):
        stats = self.system_monitor.pull_collected_stats()
        if stats is None:
            return
        batch_stats = self.get_queued_data()

        time_per_batch = 0
        if len(batch_stats) > 0 and len(batch_stats[-1]) > 1:
            i = batch_stats[-1]
            epoch_time = i[-1] - i[0]
            time_per_batch = (len(i) - 1) / epoch_time if epoch_time else 0
        stats["finished_epochs"] = len(batch_stats) - 1 if len(batch_stats) else 0
        stats["finished_batches"] = len(batch_stats[-1]) if len(batch_stats) else 0
        stats["time_per_batch"] = time_per_batch
        stats["total_batches"] = self.epoch_size
        stats["total_epochs"] = self.epochs

        systats = SystemStats(job_ref=self.job.obj_ref, **stats)
        try:
            self.connection.send_server_request("send_stats", jsonpickle.dumps(systats))
        except ConnectionError:
            logger.warning("Failed to send date to server")

    def stat_loop(self):
        with self.system_monitor:
            self.running.value = True
            while self.running.value:
                sleep(5)
                self.get_stats()


class CheckpointSender(AydaCallback):
    """
    Class for sending the checkpoints to a REST service using basic auth.
    It is implemented as Keras Callback but could
    also be used with other frameworks by calling the on_train_begin
    and on_epoch_end method.
    For this to work one have
    to set self.model to an object that implements a save(file_path) function
    """

    def __init__(self, result_service: ResultService, job_ref: str, file_path: str):
        """
        Args:
            result_service: Connection parameters used for for authorization and
                destination
            file_path: model file name path and pattern.
                You may want to place {{epoch}} into the string as epoch
                placeholder
            job_ref: Job id to identify to which job the data belongs to
        """
        self.result_service = result_service
        self.file_path = file_path
        self.metric_queue = Queue()
        self.stopped = Value("b", False)
        self.upload_process = Process()
        self.job_ref = job_ref
        self.upload_queue = Queue()
        super().__init__()

    def __upload_loop(self):

        self.stopped.value = False
        while not self.stopped.value or not self.upload_queue.empty():
            filename = self.upload_queue.get()
            if filename is None:
                continue
            with open(filename, "rb") as binary_data:
                logger.info("Grab and send new Model for " + self.job_ref)
                self.result_service.upload_model(
                    self.job_ref, basename(filename), binary_data
                )

            os.remove(filename)

    def on_epoch_end(self, epoch, _=None):
        logger.info("epoch end")
        if not self.model:
            logger.warning("Failed to save checkpoint, a model was not set")
            return
        file_name = self.file_path.format(epoch)
        logger.info("save model to " + file_name)
        self.model.save(file_name, overwrite=True)
        logger.info("epoch end")
        self.upload_queue.put(file_name)

    def on_train_begin(self, _: dict = None):
        logger.info("start train")
        self.upload_process = Process(target=self.__upload_loop)
        self.upload_process.start()

    def on_train_end(self, _: dict = None):
        self.stopped.value = True
        self.upload_queue.put(None)
        logger.info("CheckpointSender finalize")
        if self.upload_process.is_alive():
            self.upload_process.join()
        logger.info("CheckpointSender finished")


def map_log_dict_to_epochresult(
    job_ref: str, epoch: int, train_result: dict
) -> List[EpochTrainResult]:
    # convert numpy float to builtin floats
    for key, value in train_result.items():
        train_result[key] = value
    return [EpochTrainResult(epoch, job_ref, train_result)]


def create_all_result_callbacks(
    training_dir: str,
    job: JobInfo,
    connection: ServerConnection,
    result_service: ResultService,
) -> List:
    return [
        CheckpointSender(result_service, job.obj_ref, training_dir),
        MetricSender(connection, job.obj_ref),
        SystemMonitorSender(connection, job),
    ]
