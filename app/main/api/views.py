from rest_framework import parsers, viewsets, renderers, mixins, status
from rest_framework.decorators import action
from django.http import FileResponse
from rest_framework.response import Response

from main.models import \
    AIEngine, \
    Model, \
    Metric, \
    InferenceResults
from .input_serializers import \
    InputModelSerializer, \
    InputAIEngineSerializer, \
    InputMetricSerializer, \
    InputInferenceResultsSerializer
from .parsers import MultipartJsonParser


class PassthroughRenderer(renderers.BaseRenderer):
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class ZipFileRenderer(renderers.BaseRenderer):
    media_type = 'model'
    format = 'zip'

    def render(self, data, media_type=None, renderer_context=None):
        return data


def return_config_file(config_file, filename: str):
    if config_file:
        response = FileResponse(open(config_file.path, 'rb'))
        response['Content-Length'] = config_file.file.size
        response['Content-Disposition'] = f'attachment; filename={filename}.json'
        return response
    else:
        return Response({f'Config file {filename} does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class AIEngineViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = AIEngine.objects.all()
    serializer_class = InputAIEngineSerializer
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    ordering_fields = ['name', 'container_name', 'container_version', 'owner', 'data_query', 'created_at']
    ordering = '-created_at'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['name', 'container_name', 'container_version', 'owner', 'data_query']

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=(PassthroughRenderer, ZipFileRenderer),
        url_name='download_default_job_config_training_from_scratch'
    )
    def download_default_job_config_training_from_scratch(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_job_config_training_from_scratch,
            'default_job_config_training_from_scratch'
        )

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=(PassthroughRenderer, ZipFileRenderer),
        url_name='download_default_job_config_training_from_pretrained_model'
    )
    def download_default_job_config_training_from_pretrained_model(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_job_config_training_from_pretrained_model,
            'default_job_config_training_from_pretrained_model'
        )

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=(PassthroughRenderer, ZipFileRenderer),
        url_name='download_default_job_config_evaluating_from_pretrained_model'
    )
    def download_default_job_config_evaluating_from_pretrained_model(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_job_config_evaluating_from_pretrained_model,
            'default_job_config_evaluating_from_pretrained_model'
        )

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=(PassthroughRenderer, ZipFileRenderer),
        url_name='download_default_job_config_merging_models'
    )
    def download_default_job_config_merging_models(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_job_config_merging_models,
            'default_job_config_merging_models'
        )

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=(PassthroughRenderer, ZipFileRenderer),
        url_name='default_job_config_inferencing_from_pretrained_model'
    )
    def download_default_job_config_inferencing_from_pretrained_model(self, request, *args, **kwargs):
        return return_config_file(
            self.get_object().default_job_config_inferencing_from_pretrained_model,
            'default_job_config_inferencing_from_pretrained_model'
        )


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = InputModelSerializer
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    ordering_fields = ['name', 'type', 'ai_engine', 'parent_model', 'created_at', 'updated_at']
    ordering = '-created_at'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['name', 'type', 'ai_engine', 'parent_model']
    http_method_names = ['get', 'post', 'head', 'delete', 'put']  # disallow patch

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=(PassthroughRenderer, ZipFileRenderer),
        url_name='model_files'
    )
    def download_model_files(self, *args, **kwargs):
        model_files = self.get_object().model_files

        response = FileResponse(open(model_files.path, 'rb'))
        response['Content-Length'] = model_files.file.size
        response['Content-Disposition'] = 'attachment; filename=model_files.zip'
        return response

    @action(
        methods=['post'],
        detail=False,
        url_name='update_or_create'
    )
    def update_or_create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            unique_keys = {'ai_engine', 'name', 'data_hash'}
            primary_key_data = {k: v for k, v in serializer.validated_data.items() if k in unique_keys}
            other_data = {k: v for k, v in serializer.validated_data.items() if k not in unique_keys}
            obj, created = Model.objects.update_or_create(**primary_key_data, defaults=other_data)
            _status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(self.serializer_class(obj, context={'request': request}).data, status=_status)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = InputMetricSerializer
    ordering_fields = ['name', 'data_partner', 'model', 'created_at', 'updated_at']
    ordering = '-created_at'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['name', 'data_partner', 'model']
    http_method_names = ['get', 'post', 'head', 'delete', 'put']  # disallow patch

    @action(
        methods=['post'],
        detail=False,
        url_name='update_or_create'
    )
    def update_or_create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            unique_keys = {'name', 'model', 'data_hash'}
            primary_key_data = {k: v for k, v in serializer.validated_data.items() if k in unique_keys}
            other_data = {k: v for k, v in serializer.validated_data.items() if k not in unique_keys}
            obj, created = Metric.objects.update_or_create(**primary_key_data, defaults=other_data)
            _status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(self.serializer_class(obj, context={'request': request}).data, status=_status)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InferenceResultsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = InferenceResults.objects.all()
    serializer_class = InputInferenceResultsSerializer
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    ordering_fields = ['created_at']
    ordering = '-created_at'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=(PassthroughRenderer, ZipFileRenderer),
        url_name='result_files'
    )
    def download_result_files(self, *args, **kwargs):
        model_files = self.get_object().result_files

        response = FileResponse(open(model_files.path, 'rb'))
        response['Content-Length'] = model_files.file.size
        response['Content-Disposition'] = 'attachment; filename=result_files.zip'
        return response
