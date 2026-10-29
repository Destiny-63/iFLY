from django.urls import path

from apps.evaluation.views import EvaluationAPIView, TopicSpeakingAPIView

urlpatterns = [
    path("evaluation/", EvaluationAPIView.as_view(), name="evaluation"),
    path("topic-speaking/", TopicSpeakingAPIView.as_view(), name="topic-speaking"),
]
