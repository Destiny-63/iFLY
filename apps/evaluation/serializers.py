from rest_framework import serializers


class EvaluationRequestSerializer(serializers.Serializer):
    audio = serializers.FileField(required=True)
    question_text = serializers.CharField(required=True, max_length=500)
    guidance = serializers.CharField(required=True, max_length=500)

    def validate_audio(self, value):
        name = value.name.lower()
        if not (name.endswith(".mp3") or name.endswith(".pcm")):
            raise serializers.ValidationError("仅支持 .mp3 或 .pcm 文件。")
        return value


class TopicSpeakingRequestSerializer(serializers.Serializer):
    audio = serializers.FileField(required=True)
    topic = serializers.CharField(required=True, max_length=200)

    def validate_audio(self, value):
        name = value.name.lower()
        if not (name.endswith(".mp3") or name.endswith(".pcm")):
            raise serializers.ValidationError("仅支持 .mp3 或 .pcm 文件。")
        return value
