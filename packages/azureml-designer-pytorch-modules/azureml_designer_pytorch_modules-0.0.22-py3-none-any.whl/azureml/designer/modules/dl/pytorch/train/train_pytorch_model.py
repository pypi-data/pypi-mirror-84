import importlib
import os

import fire
import torch
from torchvision import transforms as t

from azureml.designer.core.model.builtin_models.pytorch.state_dict import PytorchStateDictModel
from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.designer.core.model.model_spec.builtin_model_meta.model_input import ModelInput
from azureml.designer.core.model.model_spec.builtin_model_meta.pre_processor import ImageNormalizer
from azureml.designer.core.model.model_spec.builtin_model_meta.task_type import TaskType
from azureml.designer.modules.dl.pytorch.train.trainer import trainer
from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.studio.core.io.image_schema import ImageAnnotationTypeName
from azureml.studio.core.io.model_directory import ModelDirectory, save_pytorch_state_dict_model
from azureml.studio.core.logger import TimeProfile, logger
from azureml.studio.core.error import InvalidDirectoryError
from azureml.studio.internal.error import (ErrorMapping, InvalidDatasetError,
                                           NotLabeledDatasetError, InvalidModelDirectoryError)
from azureml.studio.internal.error_handler import error_handler
from azureml.designer.modules.dl.pytorch.model_deployment.model_deployment_handler import PytorchModelDeploymentHandler


MEAN = [0.5, 0.5, 0.5]
STD = [0.5, 0.5, 0.5]
NORMALIZATION = {'mean': MEAN, 'std': STD}

TASKTYPE_TRAINER_MAPPING = {TaskType.MultiClassification.name: trainer.ClassificationTrainer.__name__}


def set_cuda_device():
    # Set os cuda visible devices to determine whether multi-gpu or single-gpu training.
    device_cnt = torch.cuda.device_count()
    logger.info(f'Found {device_cnt} cuda devices.')
    os.environ["CUDA_VISIBLE_DEVICES"] = ','.join([str(i) for i in range(device_cnt)])


def get_tensor_transform(ann_type):
    '''Get tensor transform/transforms based on annotation type.

    :param ann_type: str
    :return: (transforms.Compose, transforms.Compose)
    '''
    # 'transform' refers to a function/transform that takes in an PIL image
    # and returns a transformed version. E.g, transforms.ToTensor.
    transform = None
    # 'target_tranform' refers to a function/transform that takes in the target and transforms it.
    target_transform = None
    # transforms refers to a function/transform that takes input sample and its target as entry
    # and returns a transformed version.
    transforms = None
    if ann_type == ImageAnnotationTypeName.CLASSIFICATION:
        # Normalize to (-1, 1).
        transform = t.Compose([
            t.ToTensor(),
            t.Normalize(**NORMALIZATION),
        ])
    # TODO: support other kind of annotation type

    return transform, target_transform, transforms


def load_dataset(data_path):
    try:
        ann_type = ImageDirectory.load(data_path).get_annotation_type()
    except ValueError as e:
        ErrorMapping.rethrow(e, NotLabeledDatasetError(
            dataset_name=data_path,
            troubleshoot_hint="See https://aka.ms/aml/convert-to-image-directory and "
                              "prepare a labeled image dataset for training."))

    logger.info(f'Got annotation type: {ann_type}')
    transform, target_transform, transforms = get_tensor_transform(ann_type)
    dataset = ImageDirectory.load(data_path).to_torchvision_dataset(
        transform=transform, target_transform=target_transform, transforms=transforms)
    logger.info(f'Dataset classes: {dataset.classes}')
    return dataset, ann_type


def check_dataset(train_set, valid_set, train_ann_type, valid_ann_type):
    # TODO: validate if train and valid set have different ann type when there are tasks
    # of other kind of annotation types.
    if len(set(valid_set.classes).difference(set(train_set.classes))) > 0:
        ErrorMapping.throw(InvalidDatasetError(
            dataset1='Validation dataset',
            reason="categories of validation dataset are different from that of training dataset",
            troubleshoot_hint="Please make sure training and validation dataset have the same categories."))


def init_model(untrained_model_path, num_classes):
    logger.info("Start building model.")
    try:
        untrained_model_directory = ModelDirectory.load_instance(untrained_model_path, PytorchStateDictModel)
    except InvalidDirectoryError as e:
        ErrorMapping.rethrow(e, InvalidModelDirectoryError(
            arg_name=untrained_model_path, reason=e.reason,
            troubleshoot_hint='Please make sure input untrained model is pytorch model.'))

    task_type = untrained_model_directory.task_type
    flavor_extras = untrained_model_directory.model_meta.flavor_extras
    model_module_name = flavor_extras.get(ModelSpecConstants.MODEL_MODULE_KEY, None)
    model_module = importlib.import_module(model_module_name)
    model_class_name = flavor_extras.get(ModelSpecConstants.MODEL_CLASS_KEY, None)
    model_class = getattr(model_module, model_class_name)
    init_params = flavor_extras.get(ModelSpecConstants.INIT_PARAMS_KEY, {})
    init_params['num_classes'] = num_classes
    logger.info(f'Init model class {model_class} with parameter setting {init_params}.')
    model = model_class(**init_params)
    return model, init_params, task_type


def init_deployment_handler(train_data_path):
    with TimeProfile("Create deployment handler and inject schema and sample."):
        image_directory = ImageDirectory.load(train_data_path)
        deployment_handler = PytorchModelDeploymentHandler()
        deployment_handler.data_schema = image_directory.schema
        deployment_handler.sample_data = image_directory.get_samples()
    return deployment_handler


def save_trained_model(trained_model_path, best_model, init_params, class_to_idx, task_type, deployment_handler):
    id_to_class_dict = dict((v, k) for k, v in class_to_idx.items())
    pre_processor = ImageNormalizer(**NORMALIZATION)
    model_input = ModelInput(name='image', pre_processor=pre_processor)
    conda = {
        "name":
        "project_environment",
        "channels": ["defaults"],
        "dependencies": [
            "python=3.6.8", {
                "pip": [
                    # TODO: automatically update version
                    "azureml-designer-pytorch-modules==0.0.22",
                ]
            }
        ]
    }
    logger.info(f'Saving trained model {trained_model_path}')
    save_pytorch_state_dict_model(
        save_to=trained_model_path,
        pytorch_model=best_model,
        init_params=init_params,
        conda=conda,
        inputs=[model_input],
        task_type=task_type,
        label_map=id_to_class_dict,
        deployment_handler=deployment_handler,
    )


@error_handler
def entrance(
        untrained_model_path,
        train_data_path,
        valid_data_path,
        trained_model_path,
        epochs=5,
        batch_size=16,
        learning_rate=0.001,
        random_seed=231,
        patience=3):
    set_cuda_device()
    train_set, train_ann_type = load_dataset(train_data_path)
    valid_set, valid_ann_type = load_dataset(valid_data_path)
    check_dataset(train_set, valid_set, train_ann_type, valid_ann_type)
    # 'num_classes' will be used in model initialization.
    num_classes = train_set.num_of_classes
    model, init_params, task_type = init_model(untrained_model_path, num_classes)
    trainer_class = getattr(trainer, TASKTYPE_TRAINER_MAPPING[task_type.name], None)
    logger.info(f'Use trainer {trainer_class} for task type {task_type}.')
    task = trainer_class(model)
    with TimeProfile("Starting training"):
        best_model = task.fit(
            train_set=train_set,
            valid_set=valid_set,
            epochs=epochs,
            batch_size=batch_size,
            lr=learning_rate,
            random_seed=random_seed,
            patience=patience)

    deployment_handler = init_deployment_handler(train_data_path)

    save_trained_model(
        trained_model_path=trained_model_path,
        best_model=best_model,
        init_params=init_params,
        class_to_idx=train_set.class_to_idx,
        task_type=task_type,
        deployment_handler=deployment_handler,
    )


if __name__ == '__main__':
    fire.Fire(entrance)
