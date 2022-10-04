from rest_framework import serializers
from typing import Dict
from django.conf import settings
from typing import List
import hashlib
import random
import string

from main.models import \
    AIEngine, \
    Model, \
    Metric, \
    InferenceResults
from main.api.output_serializers import \
    OutputAIEngineSerializer, \
    OutputModelSerializer, \
    OutputMetricSerializer, \
    OutputInferenceResultsSerializer


def validate_json_file(json_file):
    # TODO implement this
    pass


def validate_zip_file(zip_file):
    # TODO implement this
    pass


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def validate_data_partners_patients(value: Dict[str, list]) -> Dict[str, list]:
    if not value:
        raise serializers.ValidationError('Data partners dict must not be empty')

    for data_partner, data_partner_patients in value.items():
        if data_partner not in settings.VALID_DATA_PARTNERS:
            raise serializers.ValidationError(
                f'All data partners must be valid. Possible values: {list(settings.VALID_DATA_PARTNERS)}')
        if not data_partner_patients:
            raise serializers.ValidationError(f'The patient ids of data partner {data_partner} is empty')
        if len(data_partner_patients) != len(set(data_partner_patients)):
            raise serializers.ValidationError(f'The patient ids of data partner {data_partner} must be different')

    return value


class InputAIEngineSerializer(serializers.ModelSerializer):
    # job_use_cases = serializers.ListField(required=True, child=serializers.CharField(max_length=100))  # TODO solve this super strange bug!!!
    job_use_cases = serializers.ListField(required=True)

    class Meta:
        model = AIEngine
        fields = '__all__'

    def validate_job_use_cases(self, value: List[str]):
        if value and isinstance(value[0], list):
            value = value[0]  # TODO solve this super strange bug!!!
        if not value:
            raise serializers.ValidationError('Job use cases list must not be empty')

        if any([use_case not in settings.VALID_JOB_USE_CASES for use_case in value]):
            raise serializers.ValidationError(f'All job use cases must be valid. Possible values: {list(settings.VALID_JOB_USE_CASES)}')

        if len(value) != len(set(value)):
            raise serializers.ValidationError(f'All job use cases must be different')

        return value

    def validate_default_job_config_training_from_scratch(self, value):
        validate_json_file(value)
        return value

    def validate_default_job_config_training_from_pretrained_model(self, value):
        validate_json_file(value)
        return value

    def validate_default_job_config_evaluating_from_pretrained_model(self, value):
        validate_json_file(value)
        return value

    def validate_default_job_config_merging_models(self, value):
        validate_json_file(value)
        return value

    def validate_default_job_config_inferencing_from_pretrained_model(self, value):
        validate_json_file(value)
        return value

    def validate(self, validated_data):
        validated_data = super().validate(validated_data)
        # TODO check container_name:container_version exists in the container registry

        # check job use cases complies with uploaded files
        job_use_cases_set = set(validated_data['job_use_cases'])
        if 'default_job_config_training_from_scratch' in validated_data.keys() and 'training_from_scratch' not in job_use_cases_set:
            raise serializers.ValidationError('Config supplied for training from scratch when it is not supported')
        if 'default_job_config_training_from_pretrained_model' in validated_data.keys() and 'training_from_pretrained_model' not in job_use_cases_set:
            raise serializers.ValidationError('Config supplied for training from pretrained model when it is not supported')
        if 'default_job_config_evaluating_from_pretrained_model' in validated_data.keys() and 'evaluating_from_pretrained_model' not in job_use_cases_set:
            raise serializers.ValidationError('Config supplied for evaluating from pretrained model when it is not supported')
        if 'default_job_config_merging_models' in validated_data.keys() and 'merging_models' not in job_use_cases_set:
            raise serializers.ValidationError('Config supplied for merging models when it is not supported')
        if 'default_job_config_inferencing_from_pretrained_model' in validated_data.keys() and 'inferencing_from_pretrained_model' not in job_use_cases_set:
            raise serializers.ValidationError('Config supplied for inferencing from pretrained model when it is not supported')

        if 'default_job_config_training_from_scratch' not in validated_data.keys() and 'training_from_scratch' in job_use_cases_set:
            raise serializers.ValidationError('Config not supplied for training from scratch when it is supported')
        if 'default_job_config_training_from_pretrained_model' not in validated_data.keys() and 'training_from_pretrained_model' in job_use_cases_set:
            raise serializers.ValidationError('Config not supplied for training from pretrained model when it is supported')
        if 'default_job_config_evaluating_from_pretrained_model' not in validated_data.keys() and 'evaluating_from_pretrained_model' in job_use_cases_set:
            raise serializers.ValidationError('Config not supplied for evaluating from pretrained model when it is supported')
        if 'default_job_config_merging_models' not in validated_data.keys() and 'merging_models' in job_use_cases_set:
            raise serializers.ValidationError('Config not supplied for merging models when it is supported')
        if 'default_job_config_inferencing_from_pretrained_model' not in validated_data.keys() and 'inferencing_from_pretrained_model' in job_use_cases_set:
            raise serializers.ValidationError('Config not supplied for inferencing from pretrained model when it is supported')

        return validated_data

    def to_representation(self, instance):
        instance = OutputAIEngineSerializer(context=self.context).to_representation(instance)
        return instance


class InputModelSerializer(serializers.ModelSerializer):
    #data_partners_patients = serializers.DictField(
    #    required=True,
    #    child=serializers.ListField(
    #        required=True,
    #        child=serializers.CharField()
    #    )
    #)
    data_partners_patients = serializers.DictField(required=True)  # TODO solve this super strange bug!!!

    class Meta:
        model = Model
        exclude = ['data_hash']

    def validate_data_partners_patients(self, data_partners_patients: Dict[str, list]) -> Dict[str, list]:
        if 'data_partners_patients' in self.initial_data:
            # return validate_data_partners_patients(data_partners_patients)
            return validate_data_partners_patients(self.initial_data['data_partners_patients'])  # TODO solve this super strange bug!!!

    def validate_model_files(self, model_files):
        validate_zip_file(model_files)
        return model_files

    def validate_parent_model(self, parent_model: Model):
        if parent_model:
            if parent_model.ai_engine.id != self.initial_data['ai_engine']:
                raise serializers.ValidationError('Parent model should be of the same AI Engine')
        return parent_model

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        if validated_data['data_partners_patients']:
            validated_data['data_hash'] = hashlib.md5(str(validated_data['data_partners_patients']).encode()).hexdigest()
        else:
            validated_data['data_hash'] = get_random_string(20)  # TODO rethink
        return validated_data

    def to_representation(self, instance):
        instance = OutputModelSerializer(context=self.context).to_representation(instance)
        return instance


class InputMetricSerializer(serializers.ModelSerializer):
    data_partner_patients = serializers.ListField(
        required=True,
        child=serializers.CharField(),
        allow_empty=False
    )

    class Meta:
        model = Metric
        exclude = ['data_hash']

    def validate_data_partner(self, data_partner: str) -> str:
        if data_partner not in settings.VALID_DATA_PARTNERS:
            raise serializers.ValidationError(f'Data partners must be valid. Possible values: {list(settings.VALID_DATA_PARTNERS)}')
        return data_partner

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        hash_object = hashlib.md5(str(f'{validated_data["data_partner"]}_{validated_data["data_partner_patients"]}').encode())
        validated_data['data_hash'] = hash_object.hexdigest()
        return validated_data

    def to_representation(self, instance):
        instance = OutputMetricSerializer(context=self.context).to_representation(instance)
        return instance


class InputInferenceResultsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='inference_results-detail')

    class Meta:
        model = InferenceResults
        fields = '__all__'

    def validate_result_files(self, result_files):
        validate_zip_file(result_files)
        return result_files

    def to_representation(self, instance):
        instance = OutputInferenceResultsSerializer(context=self.context).to_representation(instance)
        return instance
