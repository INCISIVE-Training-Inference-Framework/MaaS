from django.db import models


class AIEngine(models.Model):
    name = models.CharField(max_length=200)
    container_name = models.CharField(max_length=200)
    container_version = models.CharField(max_length=50)
    owner = models.CharField(max_length=200)
    job_use_cases = models.CharField(max_length=200)
    data_query = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    default_job_config_training_from_scratch = models.FileField(
        upload_to='ai_engines/training_from_scratch_configs',
        blank=True,
        null=True
    )
    default_job_config_training_from_pretrained_model = models.FileField(
        upload_to='ai_engines/training_from_pretrained_model_configs',
        blank=True,
        null=True
    )
    default_job_config_evaluating_from_pretrained_model = models.FileField(
        upload_to='ai_engines/evaluating_from_pretrained_model_configs',
        null=True
    )
    default_job_config_merging_models = models.FileField(
        upload_to='ai_engines/merging_models_configs',
        blank=True,
        null=True
    )
    default_job_config_inferencing_from_pretrained_model = models.FileField(
        upload_to='ai_engines/inferencing_from_pretrained_model_configs',
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('container_name', 'container_version',)


class Model(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    ai_engine = models.ForeignKey(AIEngine, on_delete=models.CASCADE)
    data_hash = models.CharField(max_length=256)
    data_partners_patients = models.TextField(null=True)
    parent_model = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model_files = models.FileField(upload_to='models')

    class Meta:
        unique_together = ('name', 'ai_engine', 'data_hash',)


class Metric(models.Model):
    name = models.CharField(max_length=200)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    data_hash = models.CharField(max_length=256)
    data_partner = models.CharField(max_length=256)
    data_partner_patients = models.TextField()
    value = models.FloatField()
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'model', 'data_hash',)


class InferenceResults(models.Model):
    execution_id = models.IntegerField()  # TODO caution for intersection between services and jobs ids
    result_files = models.FileField(upload_to='inference_results')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('execution_id',)
