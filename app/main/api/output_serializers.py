import ast

from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from main.models import \
    AIEngine, \
    AIEngineVersion, \
    AIModel, \
    EvaluationMetric, \
    GenericFile


class OutputAIEngineSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ai_engines-detail')
    id = serializers.IntegerField()
    versions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='ai_engines_versions-detail'
    )

    class Meta:
        model = AIEngine
        fields = [  # ordering
            'url',
            'id',
            'name',
            'container_name',
            'owner',
            'data_type',
            'role_type',
            'description',
            'data_considerations',
            'trl',
            'ethics',
            'caveats',
            'metrics',
            'license',
            'versions',
            'created_at',
            'updated_at'
        ]

    def to_representation(self, instance: AIEngine):
        representation = super().to_representation(instance)
        representation['data_type'] = instance.parsed_data_type
        return representation


class OutputAIEngineVersionSerializer(NestedHyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ai_engines_versions-detail')
    id = serializers.IntegerField()
    ai_engine = serializers.HyperlinkedRelatedField(view_name='ai_engines-detail', read_only=True)

    default_user_vars_training_from_scratch = serializers.HyperlinkedIdentityField(
        view_name='ai_engines_versions-download_default_user_vars_training_from_scratch',
        allow_null=True
    )
    default_user_vars_training_from_pretrained_model = serializers.HyperlinkedIdentityField(
        view_name='ai_engines_versions-download_default_user_vars_training_from_pretrained_model',
        allow_null=True
    )
    default_user_vars_evaluating_from_pretrained_model = serializers.HyperlinkedIdentityField(
        view_name='ai_engines_versions-download_default_user_vars_evaluating_from_pretrained_model',
        allow_null=True
    )
    default_user_vars_merging_models = serializers.HyperlinkedIdentityField(
        view_name='ai_engines_versions-download_default_user_vars_merging_models',
        allow_null=True
    )
    default_user_vars_inferencing_from_pretrained_model = serializers.HyperlinkedIdentityField(
        view_name='ai_engines_versions-default_user_vars_inferencing_from_pretrained_model',
        allow_null=True
    )

    class Meta:
        model = AIEngineVersion
        fields = [  # ordering
            'url',
            'id',
            'ai_engine',
            'container_version',
            'functionalities',
            'explains',
            'description',
            'default_user_vars_training_from_scratch',
            'default_user_vars_training_from_pretrained_model',
            'default_user_vars_evaluating_from_pretrained_model',
            'default_user_vars_merging_models',
            'default_user_vars_inferencing_from_pretrained_model',
            'created_at',
            'updated_at'
        ]

    def to_representation(self, instance: AIEngineVersion):
        representation = super().to_representation(instance)
        representation['functionalities'] = instance.parsed_functionalities

        functionalities_set = set(instance.parsed_functionalities)
        if 'training_from_scratch' not in functionalities_set:
            del representation['default_user_vars_training_from_scratch']
        if 'training_from_pretrained_model' not in functionalities_set:
            del representation['default_user_vars_training_from_pretrained_model']
        if 'evaluating_from_pretrained_model' not in functionalities_set:
            del representation['default_user_vars_evaluating_from_pretrained_model']
        if 'merging_models' not in functionalities_set:
            del representation['default_user_vars_merging_models']
        if 'inferencing_from_pretrained_model' not in functionalities_set:
            del representation['default_user_vars_inferencing_from_pretrained_model']

        """
        explains = Explains.objects.filter(ai_engine_version_xai=instance.id)
        url_serializer = serializers.HyperlinkedRelatedField(read_only=True, view_name='ai_engines_versions-detail')
        explains = [
            url_serializer.get_url(item.ai_engine_version_source, 'ai_engines_versions-detail', self.context.get('request'), None)
            for item in explains
        ]
        representation['explains'] = explains
        """

        return representation


class OutputAIModelSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ai_models-detail')
    id = serializers.IntegerField()
    ai_engine = serializers.SerializerMethodField()
    ai_engine_version = serializers.HyperlinkedRelatedField(
        view_name='ai_engines_versions-detail',
        read_only=True
    )
    ai_engine_version_user_vars = serializers.HyperlinkedIdentityField(
        view_name='ai_models-ai_engine_version_user_vars'
    )
    parent_ai_model = serializers.HyperlinkedRelatedField(
        view_name='ai_models-detail',
        read_only=True
    )
    contents = serializers.HyperlinkedIdentityField(view_name='ai_models-contents')

    def get_ai_engine(self, instance):
        return serializers.HyperlinkedRelatedField(
            view_name='ai_engines-detail',
            read_only=True
        ).get_url(instance.ai_engine_version.ai_engine, 'ai_engines-detail', self.context.get('request'), None)

    class Meta:
        model = AIModel
        fields = [  # ordering
            'url',
            'id',
            'name',
            'ai_engine',
            'ai_engine_version',
            'ai_engine_version_user_vars',
            'data_partners_patients',
            'merge_type',
            'parent_ai_model',
            'description',
            'contents',
            'created_at',
            'updated_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['data_partners_patients']:
            representation['data_partners_patients'] = instance.parsed_data_partners_patients
        return representation


class OutputEvaluationMetricSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='evaluation_metrics-detail')
    id = serializers.IntegerField()
    ai_engine = serializers.SerializerMethodField()
    ai_engine_version = serializers.SerializerMethodField()
    ai_model = serializers.HyperlinkedRelatedField(
        view_name='ai_models-detail',
        read_only=True
    )

    def get_ai_engine(self, instance):
        return serializers.HyperlinkedRelatedField(
            view_name='ai_engines-detail',
            read_only=True
        ).get_url(instance.ai_model.ai_engine_version.ai_engine, 'ai_engines-detail', self.context.get('request'), None)

    def get_ai_engine_version(self, instance):
        return serializers.HyperlinkedRelatedField(
            view_name='ai_engines_versions-detail',
            read_only=True
        ).get_url(instance.ai_model.ai_engine_version, 'ai_engines_versions-detail', self.context.get('request'), None)

    class Meta:
        model = EvaluationMetric
        fields = [
            'url',
            'id',
            'name',
            'ai_engine',
            'ai_engine_version',
            'ai_model',
            'data_partners_patients',
            'value',
            'description',
            'created_at',
            'updated_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['data_partners_patients']:
            representation['data_partners_patients'] = instance.parsed_data_partners_patients
        return representation


class OutputGenericFileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='generic_files-detail')
    id = serializers.IntegerField()
    listed_contents = serializers.HyperlinkedIdentityField(view_name='generic_files-list')
    individual_contents_download = serializers.HyperlinkedIdentityField(view_name='generic_files-get')
    packed_contents_download = serializers.HyperlinkedIdentityField(view_name='generic_files-packed')

    class Meta:
        model = GenericFile
        fields = [
            'url',
            'id',
            'name',
            'listed_contents',
            'individual_contents_download',
            'packed_contents_download',
            'created_at'
        ]
