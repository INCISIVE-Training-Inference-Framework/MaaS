import os
import ast
import string
import random
from functools import partial

from django.db import models


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class AIEngine(models.Model):
    name = models.CharField(max_length=200, unique=True)
    container_name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    description = models.TextField()
    data_type = models.TextField()
    role_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # trl-cars, ai passport
    data_considerations = models.TextField(null=True)
    trl = models.CharField(max_length=200, null=True)
    ethics = models.TextField(null=True)
    caveats = models.TextField(null=True)
    metrics = models.TextField(null=True)
    license = models.CharField(max_length=200, null=True)

    @property
    def parsed_data_type(self) -> list:
        if isinstance(self.data_type, list):
            return self.data_type
        return ast.literal_eval(self.data_type)


def ai_engine_version_user_vars_path(use_case, instance, filename):
    _, file_extension = os.path.splitext(filename)
    return f'ai_engine_version/' \
           f'user_vars/' \
           f'{use_case}/' \
           f'{instance.ai_engine.name}_{instance.container_version}{file_extension}'


class AIEngineVersion(models.Model):
    ai_engine = models.ForeignKey(AIEngine, related_name='versions', on_delete=models.CASCADE)
    container_version = models.CharField(max_length=50)
    description = models.TextField()
    functionalities = models.TextField()
    explains = models.BooleanField()
    # Define the maximum iteration time allowed for an AI Engine to complete its task
    max_iteration_time = models.IntegerField(default=1200)
    # Define memory request and limit. Accepted quantity suffixes
    #   --> E, P, T, G, M, k
    #   --> Or power-of-two equivalents: Ei, Pi, Ti, Gi, Mi, Ki
    memory_request = models.CharField(default='3584Mi')
    memory_limit = models.CharField(default='3584Mi')
    # Define CPU request and limit. Accepted quantity suffixes
    #   --> m (millicpu) equivalent to 0.1 CPU
    cpu_request = models.CharField(default='250m')
    cpu_limit = models.CharField(default='4000m')

    default_user_vars_training_from_scratch = models.FileField(
        upload_to=partial(ai_engine_version_user_vars_path, 'training_from_scratch'),
        null=True,
        max_length=300  # defines max size of the full path, if it is over it, the filename is shortened automatically
    )
    default_user_vars_training_from_pretrained_model = models.FileField(
        upload_to=partial(ai_engine_version_user_vars_path, 'training_from_pretrained_model'),
        null=True,
        max_length=300
    )
    default_user_vars_evaluating_from_pretrained_model = models.FileField(
        upload_to=partial(ai_engine_version_user_vars_path, 'evaluating_from_pretrained_model'),
        null=True,
        max_length=300
    )
    default_user_vars_merging_models = models.FileField(
        upload_to=partial(ai_engine_version_user_vars_path, 'merging_models'),
        null=True,
        max_length=300
    )
    default_user_vars_inferencing_from_pretrained_model = models.FileField(
        upload_to=partial(ai_engine_version_user_vars_path, 'inferencing_from_pretrained_model'),
        null=True,
        max_length=300
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('ai_engine', 'container_version')

    @property
    def parsed_functionalities(self) -> list:
        if isinstance(self.functionalities, list):
            return self.functionalities
        return ast.literal_eval(self.functionalities)


def ai_model_user_vars_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return f'ai_model/' \
           f'user_vars/' \
           f'{instance.name}_{instance.ai_engine_version.container_version}{file_extension}'


def ai_model_contents_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return f'ai_model/' \
           f'contents/' \
           f'{instance.name}_{instance.ai_engine_version.container_version}{file_extension}'


class AIModel(models.Model):
    ai_engine_version = models.ForeignKey(AIEngineVersion, on_delete=models.CASCADE)
    ai_engine_version_user_vars = models.FileField(upload_to=ai_model_user_vars_path, max_length=300)
    name = models.CharField(max_length=200)
    data_hash = models.CharField(max_length=256, null=True)
    data_partners_patients = models.TextField(null=True)
    merge_type = models.CharField(max_length=50, null=True)
    parent_ai_model = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    contents = models.FileField(upload_to=ai_model_contents_path, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Define number of retries when downloading the model (required for large models)
    download_resume_retries = models.IntegerField(default=4)

    class Meta:
        unique_together = ('name', 'ai_engine_version', 'data_hash')

    @property
    def parsed_data_partners_patients(self) -> dict:
        if isinstance(self.data_partners_patients, dict):
            return self.data_partners_patients
        return ast.literal_eval(self.data_partners_patients)


class EvaluationMetric(models.Model):
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    data_hash = models.CharField(max_length=256)
    data_partners_patients = models.TextField()
    value = models.FloatField()
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'ai_model', 'data_hash')

    @property
    def parsed_data_partners_patients(self) -> dict:
        if isinstance(self.data_partners_patients, dict):
            return self.data_partners_patients
        return ast.literal_eval(self.data_partners_patients)


def generic_file_contents_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return f'generic_file/' \
           f'contents/' \
           f'{instance.name}{file_extension}'


class GenericFile(models.Model):
    name = models.CharField(max_length=200)
    contents = models.FileField(upload_to=generic_file_contents_path)
    created_at = models.DateTimeField(auto_now_add=True)
