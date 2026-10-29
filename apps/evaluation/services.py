from services.audio_processor import AudioProcessor
from services.ise_service import ISEService
from services.spark_service import SparkService


class EvaluationPipeline:
    def __init__(self) -> None:
        self.audio_processor = AudioProcessor()
        self.ise_service = ISEService()
        self.spark_service = SparkService()
