import logging
import zipfile

from django.http import FileResponse, JsonResponse
from rest_framework import parsers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import \
    AIEngine, \
    AIEngineVersion, \
    AIModel, \
    EvaluationMetric, \
    GenericFile
from .input_serializers import \
    InputAIEngineSerializer, \
    InputAIEngineUpdateSerializer, \
    InputAIEngineVersionSerializer, \
    InputAIEngineVersionUpdateSerializer, \
    InputAIModelSerializer, \
    InputAIModelUpdateSerializer, \
    InputEvaluationMetricSerializer, \
    InputEvaluationMetricUpdateSerializer, \
    InputGenericFileSerializer
from .parsers import MultipartJsonParser as OwnMultipartJsonParser

logger = logging.getLogger(__name__)


def return_config_file(config_file, filename: str):
    if config_file:
        response = FileResponse(open(config_file.path, 'rb'))
        response['Content-Length'] = config_file.file.size
        response['Content-Type'] = 'application/json'
        response['Content-Disposition'] = f'attachment; filename={filename}.json'
        return response
    else:
        response = Response({f'Config file {filename} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        logger.error(response.data)
        return response


class AIEngineViewSet(viewsets.ModelViewSet):
    queryset = AIEngine.objects.all()
    serializer_class = InputAIEngineSerializer
    parser_classes = [parsers.JSONParser]
    ordering_fields = ['name', 'container_name', 'owner', 'data_type', 'role_type', 'created_at', 'update_at']
    ordering = '-created_at'
    filterset_fields = ['name', 'container_name', 'owner', 'data_type', 'role_type']
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']  # disallow put

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = InputAIEngineUpdateSerializer

        return serializer_class


class AIEngineVersionViewSet(viewsets.ModelViewSet):
    queryset = AIEngineVersion.objects.all()
    serializer_class = InputAIEngineVersionSerializer
    parser_classes = [OwnMultipartJsonParser]
    ordering_fields = ['ai_engine', 'container_version', 'created_at', 'update_at']
    ordering = '-created_at'
    filterset_fields = ['ai_engine', 'container_version']
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']  # disallow put

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = InputAIEngineVersionUpdateSerializer

        return serializer_class

    @action(
        methods=['get'],
        detail=True,
        url_name='download_default_user_vars_training_from_scratch'
    )
    def download_default_user_vars_training_from_scratch(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_user_vars_training_from_scratch,
            'default_user_vars_training_from_scratch'
        )

    @action(
        methods=['get'],
        detail=True,
        url_name='download_default_user_vars_training_from_pretrained_model'
    )
    def download_default_user_vars_training_from_pretrained_model(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_user_vars_training_from_pretrained_model,
            'default_user_vars_training_from_pretrained_model'
        )

    @action(
        methods=['get'],
        detail=True,
        url_name='download_default_user_vars_evaluating_from_pretrained_model'
    )
    def download_default_user_vars_evaluating_from_pretrained_model(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_user_vars_evaluating_from_pretrained_model,
            'default_user_vars_evaluating_from_pretrained_model'
        )

    @action(
        methods=['get'],
        detail=True,
        url_name='download_default_user_vars_merging_models'
    )
    def download_user_vars_config_merging_models(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_user_vars_merging_models,
            'default_user_vars_merging_models'
        )

    @action(
        methods=['get'],
        detail=True,
        url_name='default_user_vars_inferencing_from_pretrained_model'
    )
    def download_default_user_vars_inferencing_from_pretrained_model(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_user_vars_inferencing_from_pretrained_model,
            'default_user_vars_inferencing_from_pretrained_model'
        )


class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = InputAIModelSerializer
    parser_classes = [OwnMultipartJsonParser]
    ordering_fields = ['ai_engine_version', 'name', 'merge_type', 'parent_ai_model', 'created_at', 'updated_at']
    ordering = '-created_at'
    filterset_fields = ['ai_engine_version', 'name', 'merge_type', 'parent_ai_model']
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']  # disallow put

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = InputAIModelUpdateSerializer

        return serializer_class

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if 'ai_engine' in self.request.query_params:
            filter_by_ai_engine = int(self.request.query_params['ai_engine'])
            queryset = queryset.filter(ai_engine_version__ai_engine=filter_by_ai_engine)
        return queryset

    @action(
        methods=['get'],
        detail=True,
        url_name='ai_engine_version_user_vars'
    )
    def download_ai_engine_version_user_vars(self, *args, **kwargs):
        return return_config_file(
            self.get_object().ai_engine_version_user_vars,
            'ai_engine_version_user_vars'
        )

    @action(
        methods=['get'],
        detail=True,
        url_name='contents'
    )
    def download_contents(self, *args, **kwargs):
        contents = self.get_object().contents

        response = FileResponse(open(contents.path, 'rb'))
        response['Content-Length'] = contents.file.size
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=ai_model.zip'
        return response

    @action(
        methods=['post'],
        detail=False,
        url_name='update_or_create'
    )
    def update_or_create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.context['validate_pk_unique'] = False
        if serializer.is_valid():
            unique_keys = {'ai_engine', 'name', 'data_hash'}
            primary_key_data = {k: v for k, v in serializer.validated_data.items() if k in unique_keys}
            other_data = {k: v for k, v in serializer.validated_data.items() if k not in unique_keys}
            obj, created = AIModel.objects.update_or_create(**primary_key_data, defaults=other_data)
            _status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(self.serializer_class(obj, context={'request': request}).data, status=_status)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.error(response.data)
            return response


class MetricViewSet(viewsets.ModelViewSet):
    queryset = EvaluationMetric.objects.all()
    serializer_class = InputEvaluationMetricSerializer
    ordering_fields = ['ai_model', 'name', 'value', 'created_at', 'updated_at']
    ordering = '-created_at'
    filterset_fields = ['ai_model', 'name', 'value']
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']  # disallow put

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = InputEvaluationMetricUpdateSerializer

        return serializer_class

    @action(
        methods=['post'],
        detail=False,
        url_name='update_or_create'
    )
    def update_or_create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            unique_keys = {'name', 'ai_model', 'data_hash'}
            primary_key_data = {k: v for k, v in serializer.validated_data.items() if k in unique_keys}
            other_data = {k: v for k, v in serializer.validated_data.items() if k not in unique_keys}
            obj, created = EvaluationMetric.objects.update_or_create(**primary_key_data, defaults=other_data)
            _status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(self.serializer_class(obj, context={'request': request}).data, status=_status)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.error(response.data)
            return response


class GenericFilesViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = GenericFile.objects.all()
    serializer_class = InputGenericFileSerializer
    parser_classes = [OwnMultipartJsonParser]
    filterset_fields = ['name']
    ordering_fields = ['created_at']
    ordering = '-created_at'

    def list_contents(self) -> set:
        contents = zipfile.ZipFile(self.get_object().contents.path)
        return {name for name in contents.namelist() if not name.endswith('/')}

    @action(
        methods=['get'],
        detail=True,
        url_name='list',
        url_path='listed_contents'
    )
    def listed_contents(self, *args, **kwargs):
        contents = self.list_contents()
        response = JsonResponse({'listed_contents': list(contents)})
        return response

    @action(
        methods=['get'],
        detail=True,
        url_name='get',
        url_path='individual_contents_download'
    )
    def individual_contents_download(self, request, *args, **kwargs):
        file_path = request.query_params.get('file_path')

        if file_path:
            contents = self.list_contents()
            if file_path not in contents:
                response = Response({f'{file_path} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
                logger.error(response.data)
                return response

            file = zipfile.ZipFile(self.get_object().contents.path).open(file_path)
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename={file_path}'
            return response
        else:
            response = Response({f'Query parameter file_path not specified'}, status=status.HTTP_400_BAD_REQUEST)
            logger.error(response.data)
            return response

    @action(
        methods=['get'],
        detail=True,
        url_name='packed',
        url_path='packed_contents_download'
    )
    def packed_contents_download(self, *args, **kwargs):
        contents = self.get_object().contents

        response = FileResponse(open(contents.path, 'rb'))
        response['Content-Length'] = contents.file.size
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=packed_contents.zip'
        return response

