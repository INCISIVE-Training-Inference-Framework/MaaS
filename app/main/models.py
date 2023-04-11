import ast

from django.db import models


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


class AIEngineVersion(models.Model):
    ai_engine = models.ForeignKey(AIEngine, related_name='versions', on_delete=models.CASCADE)
    container_version = models.CharField(max_length=50)
    description = models.TextField()
    functionalities = models.TextField()
    explains = models.BooleanField()
    default_user_vars_training_from_scratch = models.FileField(
        upload_to='ai_engines/training_from_scratch_user_vars',
        null=True
    )
    default_user_vars_training_from_pretrained_model = models.FileField(
        upload_to='ai_engines/training_from_pretrained_model_user_vars',
        null=True
    )
    default_user_vars_evaluating_from_pretrained_model = models.FileField(
        upload_to='ai_engines/evaluating_from_pretrained_model_user_vars',
        null=True
    )
    default_user_vars_merging_models = models.FileField(
        upload_to='ai_engines/merging_models_user_vars',
        null=True
    )
    default_user_vars_inferencing_from_pretrained_model = models.FileField(
        upload_to='ai_engines/inferencing_from_pretrained_model_user_vars',
        null=True
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


class AIModel(models.Model):
    ai_engine_version = models.ForeignKey(AIEngineVersion, on_delete=models.CASCADE)
    ai_engine_version_user_vars = models.FileField(upload_to='ai_models/user_vars')
    name = models.CharField(max_length=200)
    data_hash = models.CharField(max_length=256, null=True)
    data_partners_patients = models.TextField(null=True)
    merge_type = models.CharField(max_length=50, null=True)
    parent_ai_model = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    contents = models.FileField(upload_to='ai_models/contents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class GenericFile(models.Model):
    name = models.CharField(max_length=200)
    contents = models.FileField(upload_to='generic_files')
    created_at = models.DateTimeField(auto_now_add=True)
