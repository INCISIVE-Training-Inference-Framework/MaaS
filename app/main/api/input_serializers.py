import hashlib
import random
import string
from typing import Dict

from django.conf import settings
from rest_framework import serializers

from main.api.output_serializers import \
    OutputAIEngineSerializer, \
    OutputAIEngineVersionSerializer, \
    OutputAIModelSerializer, \
    OutputEvaluationMetricSerializer, \
    OutputGenericFileSerializer
from main.models import \
    AIEngine, \
    AIEngineVersion, \
    AIModel, \
    EvaluationMetric, \
    GenericFile


def validate_json_file(json_file):
    # TODO implement this
    pass


def validate_zip_file(zip_file):
    # TODO implement this
    pass


def validate_data_partners_patients(value: Dict[str, list]) -> Dict[str, list]:
    found_error = False
    message_error = {}
    for data_partner, data_partner_patients in value.items():
        if data_partner not in settings.VALID_DATA_PARTNERS:
            found_error = True
            message_error[data_partner] = [f'\"{data_partner}\" is not a valid choice. Possible values: {list(settings.VALID_DATA_PARTNERS)}']
            continue
        if data_partner_patients is None:
            found_error = True
            message_error[data_partner] = [f'\"{data_partner_patients}\" is null.']
            continue
        if not isinstance(data_partner_patients, list):
            found_error = True
            message_error[data_partner] = [f'\"{data_partner_patients}\" is not a list.']
            continue
        if len(data_partner_patients) == 0:
            found_error = True
            message_error[data_partner] = [f'the list is empty.']
            continue
        if len(data_partner_patients) != len(set(data_partner_patients)):
            found_error = True
            message_error[data_partner] = [f'the list contains duplicates.']

        value[data_partner] = [str(item) for item in data_partner_patients]

    if found_error:
        raise serializers.ValidationError(message_error)
    else:
        return value


class InputAIEngineSerializer(serializers.ModelSerializer):
    data_type = serializers.ListField(required=True, allow_empty=False, child=serializers.ChoiceField(choices=settings.VALID_AI_ENGINE_DATA_TYPES))  # TODO check not repeated items
    role_type = serializers.ChoiceField(choices=settings.VALID_AI_ENGINE_ROLE_TYPES)

    class Meta:
        model = AIEngine
        fields = '__all__'

    def validate_container_name(self, value: str):
        # TODO validate that is exists on the docker registry
        return value

    def to_representation(self, instance):
        instance = OutputAIEngineSerializer(context=self.context).to_representation(instance)
        return instance


class InputAIEngineUpdateSerializer(serializers.ModelSerializer):
    data_type = serializers.ListField(required=True, allow_empty=False, child=serializers.ChoiceField(choices=settings.VALID_AI_ENGINE_DATA_TYPES))
    role_type = serializers.ChoiceField(choices=settings.VALID_AI_ENGINE_ROLE_TYPES)

    class Meta:
        model = AIEngine
        exclude = ['container_name']

    def validate_data_type(self, value: list):
        unique_items = set(value)
        if len(unique_items) != len(value):
            raise serializers.ValidationError('it contains repeated items')
        return value

    def to_representation(self, instance):
        instance = OutputAIEngineSerializer(context=self.context).to_representation(instance)
        return instance


class InputAIEngineVersionSerializer(serializers.ModelSerializer):
    functionalities = serializers.ListField(required=True, allow_empty=False, child=serializers.ChoiceField(choices=settings.VALID_AI_ENGINE_FUNCTIONALITIES))
    # explains = serializers.ListField(required=False, allow_empty=True, default=[])
    explains = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = AIEngineVersion
        fields = '__all__'

    def validate_container_version(self, value: str):
        # TODO validate that is exists on the docker registry
        return value

    def validate_functionalities(self, value: list):
        unique_items = set(value)
        if len(unique_items) != len(value):
            raise serializers.ValidationError('it contains repeated items')
        return value

    def validate_default_user_vars_training_from_scratch(self, value):
        validate_json_file(value)
        return value

    def validate_default_user_vars_training_from_pretrained_model(self, value):
        validate_json_file(value)
        return value

    def validate_default_user_vars_evaluating_from_pretrained_model(self, value):
        validate_json_file(value)
        return value

    def validate_default_user_vars_merging_models(self, value):
        validate_json_file(value)
        return value

    def validate_default_user_vars_inferencing_from_pretrained_model(self, value):
        validate_json_file(value)
        return value

    def validate_max_iteration_time(self, value):
        if value <= 0:
            raise serializers.ValidationError('it must be greater than 0')
        return value

    def validate(self, validated_data):
        validated_data = super().validate(validated_data)

        # check functionalities complies with uploaded files
        if 'functionalities' in validated_data:
            functionalities_set = set(validated_data['functionalities'])
            if 'default_user_vars_training_from_scratch' in validated_data.keys() and 'training_from_scratch' not in functionalities_set:
                raise serializers.ValidationError('User vars were supplied for training from scratch when it is not supported')
            if 'default_user_vars_training_from_pretrained_model' in validated_data.keys() and 'training_from_pretrained_model' not in functionalities_set:
                raise serializers.ValidationError('User vars were supplied for training from pretrained model when it is not supported')
            if 'default_user_vars_evaluating_from_pretrained_model' in validated_data.keys() and 'evaluating_from_pretrained_model' not in functionalities_set:
                raise serializers.ValidationError('User vars were supplied for evaluating from pretrained model when it is not supported')
            if 'default_user_vars_merging_models' in validated_data.keys() and 'merging_models' not in functionalities_set:
                raise serializers.ValidationError('User vars were supplied for merging models when it is not supported')
            if 'default_user_vars_inferencing_from_pretrained_model' in validated_data.keys() and 'inferencing_from_pretrained_model' not in functionalities_set:
                raise serializers.ValidationError('User vars were supplied for inferencing from pretrained model when it is not supported')

            if 'default_user_vars_training_from_scratch' not in validated_data.keys() and 'training_from_scratch' in functionalities_set:
                raise serializers.ValidationError('User vars not supplied for training from scratch when it is supported')
            if 'default_user_vars_training_from_pretrained_model' not in validated_data.keys() and 'training_from_pretrained_model' in functionalities_set:
                raise serializers.ValidationError('User vars not supplied for training from pretrained model when it is supported')
            if 'default_user_vars_evaluating_from_pretrained_model' not in validated_data.keys() and 'evaluating_from_pretrained_model' in functionalities_set:
                raise serializers.ValidationError('User vars not supplied for evaluating from pretrained model when it is supported')
            if 'default_user_vars_merging_models' not in validated_data.keys() and 'merging_models' in functionalities_set:
                raise serializers.ValidationError('User vars not supplied for merging models when it is supported')
            if 'default_user_vars_inferencing_from_pretrained_model' not in validated_data.keys() and 'inferencing_from_pretrained_model' in functionalities_set:
                raise serializers.ValidationError('User vars not supplied for inferencing from pretrained model when it is supported')

        return validated_data

    def to_representation(self, instance):
        instance = OutputAIEngineVersionSerializer(context=self.context).to_representation(instance)
        return instance


class InputAIEngineVersionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIEngineVersion
        fields = ['description']

    def to_representation(self, instance):
        instance = OutputAIEngineVersionSerializer(context=self.context).to_representation(instance)
        return instance


class InputAIModelSerializer(serializers.ModelSerializer):
    data_partners_patients = serializers.DictField(required=False, allow_empty=False)

    class Meta:
        model = AIModel
        exclude = ['data_hash']

    def validate_ai_engine_version_user_vars(self, value):
        validate_json_file(value)
        return value

    def validate_data_partners_patients(self, value):
        return validate_data_partners_patients(value)

    def validate_parent_ai_model(self, value: AIModel):
        # TODO validate its from same AI Engine
        return value

    def validate_contents(self, value):
        validate_zip_file(value)
        return value

    def validate_download_resume_retries(self, value):
        if value <= 0:
            raise serializers.ValidationError('it must be greater than 0')
        return value

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        if 'data_partners_patients' in validated_data:
            validated_data['data_hash'] = hashlib.md5(str(validated_data['data_partners_patients']).encode()).hexdigest()
        else:
            validated_data['data_hash'] = None
        return validated_data

    def validate(self, validated_data):
        validated_data = super().validate(validated_data)

        # enforce unique together clause -> Django will not do it because of the nullable field
        if 'validate_pk_unique' not in self.context or self.context['validate_pk_unique']:  # due to update_or_create action
            if validated_data['data_hash'] is not None:
                if AIModel.objects.filter(
                        name=validated_data['name'],
                        ai_engine_version=validated_data['ai_engine_version'],
                        data_hash=validated_data['data_hash']
                ).exists():
                    raise serializers.ValidationError('The fields name, ai_engine_version and data_partners_patients must make a unique set.')

        return validated_data

    def to_representation(self, instance):
        instance = OutputAIModelSerializer(context=self.context).to_representation(instance)
        return instance


class InputAIModelUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIModel
        fields = ['merge_type', 'description']

    def to_representation(self, instance):
        instance = OutputAIModelSerializer(context=self.context).to_representation(instance)
        return instance


class InputEvaluationMetricSerializer(serializers.ModelSerializer):
    data_partners_patients = serializers.DictField(required=True, allow_empty=False)

    class Meta:
        model = EvaluationMetric
        exclude = ['data_hash']

    def validate_data_partners_patients(self, value):
        return validate_data_partners_patients(value)

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        validated_data['data_hash'] = hashlib.md5(str(validated_data['data_partners_patients']).encode()).hexdigest()

        return validated_data

    def to_representation(self, instance):
        instance = OutputEvaluationMetricSerializer(context=self.context).to_representation(instance)
        return instance


class InputEvaluationMetricUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EvaluationMetric
        fields = [
            'value',
            'description'
        ]

    def to_representation(self, instance):
        instance = OutputEvaluationMetricSerializer(context=self.context).to_representation(instance)
        return instance


class InputGenericFileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GenericFile
        fields = '__all__'

    def validate_contents(self, value):
        validate_zip_file(value)
        return value

    def to_representation(self, instance):
        instance = OutputGenericFileSerializer(context=self.context).to_representation(instance)
        return instance
