from rest_framework import serializers
import ast

from main.models import \
    AIEngine, \
    Model, \
    Metric, \
    InferenceResults


class OutputAIEngineSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ai_engines-detail')
    id = serializers.IntegerField()
    default_job_config_training_from_scratch = serializers.HyperlinkedIdentityField(
        view_name='ai_engines-download_default_job_config_training_from_scratch',
        allow_null=True
    )
    default_job_config_training_from_pretrained_model = serializers.HyperlinkedIdentityField(
        view_name='ai_engines-download_default_job_config_training_from_pretrained_model',
        allow_null=True
    )
    default_job_config_evaluating_from_pretrained_model = serializers.HyperlinkedIdentityField(
        view_name='ai_engines-download_default_job_config_evaluating_from_pretrained_model',
        allow_null=True
    )
    default_job_config_merging_models = serializers.HyperlinkedIdentityField(
        view_name='ai_engines-download_default_job_config_merging_models',
        allow_null=True
    )
    default_job_config_inferencing_from_pretrained_model = serializers.HyperlinkedIdentityField(
        view_name='ai_engines-default_job_config_inferencing_from_pretrained_model',
        allow_null=True
    )

    class Meta:
        model = AIEngine
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['job_use_cases'] = ast.literal_eval(representation['job_use_cases'])

        # ignore null files
        if not instance.default_job_config_training_from_scratch:
            representation.pop('default_job_config_training_from_scratch')
        if not instance.default_job_config_training_from_pretrained_model:
            representation.pop('default_job_config_training_from_pretrained_model')
        if not instance.default_job_config_evaluating_from_pretrained_model:
            representation.pop('default_job_config_evaluating_from_pretrained_model')
        if not instance.default_job_config_merging_models:
            representation.pop('default_job_config_merging_models')
        if not instance.default_job_config_inferencing_from_pretrained_model:
            representation.pop('default_job_config_inferencing_from_pretrained_model')
        return representation


class OutputModelSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='models-detail')
    id = serializers.IntegerField()
    ai_engine = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='ai_engines-detail',
        queryset=AIEngine.objects.all()
    )
    parent_model = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='models-detail',
        queryset=Model.objects.all()
    )
    model_files = serializers.HyperlinkedIdentityField(view_name='models-model_files')

    class Meta:
        model = Model
        exclude = ['data_hash']

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        if instance['data_partners_patients']:
            instance['data_partners_patients'] = ast.literal_eval(instance['data_partners_patients'])
        return instance


class OutputMetricSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='metrics-detail')
    id = serializers.IntegerField()
    model = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='models-detail',
        queryset=Model.objects.all()
    )

    class Meta:
        model = Metric
        exclude = ['data_hash']

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance['data_partner_patients'] = ast.literal_eval(instance['data_partner_patients'])
        return instance


class OutputInferenceResultsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='inference_results-detail')
    id = serializers.IntegerField()
    result_files = serializers.HyperlinkedIdentityField(view_name='inference_results-result_files')

    class Meta:
        model = InferenceResults
        fields = '__all__'
