from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework.test import APIClient


class EvaluationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("apps.evaluation.views.SparkService")
    @patch("apps.evaluation.views.ISEService")
    @patch("apps.evaluation.views.AudioProcessor")
    def test_evaluation_success_stream(
        self, audio_cls, ise_cls, spark_cls
    ):
        audio = audio_cls.return_value
        audio.save_upload_to_temp.return_value = MagicMock()
        audio.ensure_pcm.return_value = MagicMock()

        ise = ise_cls.return_value
        ise.evaluate.return_value = {
            "total_score": 90.0,
            "accuracy_score": 92.0,
            "fluency_score": 88.0,
            "integrity_score": 91.0,
        }

        spark = spark_cls.return_value
        spark.stream_feedback.return_value = iter(["建议一。", "建议二。"])

        response = self.client.post(
            "/api/evaluation/",
            {
                "question_text": "今天天气怎么样",
                "guidance": "关注声调",
                "audio": self._dummy_pcm(),
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 200)
        content = b"".join(response.streaming_content).decode("utf-8")
        self.assertIn('"type": "evaluation"', content)
        self.assertIn('"type": "feedback_chunk"', content)
        self.assertIn('"type": "done"', content)

    def test_evaluation_invalid_file_extension(self):
        response = self.client.post(
            "/api/evaluation/",
            {
                "question_text": "今天天气怎么样",
                "guidance": "关注声调",
                "audio": self._dummy_txt(),
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("audio", response.data)

    @staticmethod
    def _dummy_pcm():
        from django.core.files.uploadedfile import SimpleUploadedFile

        return SimpleUploadedFile("sample.pcm", b"\x00" * 32000)

    @staticmethod
    def _dummy_txt():
        from django.core.files.uploadedfile import SimpleUploadedFile

        return SimpleUploadedFile("sample.txt", b"not audio")
