import shutil
import tempfile
from pathlib import Path

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError


class AudioFormatError(Exception):
    pass


class AudioProcessor:
    TARGET_RATE = 16000
    TARGET_CHANNELS = 1
    TARGET_WIDTH = 2  # 16-bit
    MAX_DURATION_SECONDS = 180

    def save_upload_to_temp(self, uploaded_file) -> Path:
        suffix = Path(uploaded_file.name).suffix.lower() or ".bin"
        fd, temp_path = tempfile.mkstemp(prefix="upload_", suffix=suffix)
        Path(temp_path).write_bytes(b"")
        with open(fd, "wb", closefd=True) as handle:
            for chunk in uploaded_file.chunks():
                handle.write(chunk)
        return Path(temp_path)

    def ensure_pcm(self, source_path: Path) -> Path:
        suffix = source_path.suffix.lower()
        if suffix == ".pcm":
            self._validate_pcm_duration(source_path)
            return source_path
        if suffix == ".mp3":
            return self._convert_mp3_to_pcm(source_path)
        raise AudioFormatError("仅支持 .mp3 或 .pcm 文件。")

    def cleanup_temp_file(self, path: Path) -> None:
        if path and path.exists():
            path.unlink(missing_ok=True)

    def get_duration_seconds(self, path: Path) -> float:
        """获取音频时长（秒）。支持 .mp3 和 .pcm。"""
        suffix = path.suffix.lower()
        if suffix == ".pcm":
            return path.stat().st_size / (
                self.TARGET_RATE * self.TARGET_CHANNELS * self.TARGET_WIDTH
            )
        if suffix == ".mp3":
            audio = AudioSegment.from_mp3(path.as_posix())
            return len(audio) / 1000
        raise AudioFormatError("仅支持 .mp3 或 .pcm 文件。")

    def _validate_pcm_duration(self, pcm_path: Path) -> None:
        # raw PCM duration = bytes / (sample_rate * channels * sample_width)
        duration = pcm_path.stat().st_size / (
            self.TARGET_RATE * self.TARGET_CHANNELS * self.TARGET_WIDTH
        )
        if duration > self.MAX_DURATION_SECONDS:
            raise AudioFormatError("音频时长超过 3 分钟限制。")

    def _convert_mp3_to_pcm(self, mp3_path: Path) -> Path:
        # 检查 ffmpeg 是否可用
        if not shutil.which("ffmpeg"):
            raise AudioFormatError(
                "未检测到 ffmpeg，请先安装并加入 PATH。\n"
                "Windows: 下载 https://ffmpeg.org/download.html 并添加到 PATH\n"
                "或者直接使用 .pcm 格式文件（无需转换）"
            )
        
        try:
            audio = AudioSegment.from_mp3(mp3_path.as_posix())
        except CouldntDecodeError as exc:
            raise AudioFormatError("MP3 解码失败，请检查文件是否损坏。") from exc
        except Exception as exc:
            raise AudioFormatError(f"MP3 转换失败: {exc}") from exc

        duration_sec = len(audio) / 1000
        if duration_sec > self.MAX_DURATION_SECONDS:
            raise AudioFormatError("音频时长超过 3 分钟限制。")

        processed = (
            audio.set_frame_rate(self.TARGET_RATE)
            .set_channels(self.TARGET_CHANNELS)
            .set_sample_width(self.TARGET_WIDTH)
        )

        fd, out_path = tempfile.mkstemp(prefix="converted_", suffix=".pcm")
        Path(out_path).write_bytes(b"")
        with open(fd, "wb", closefd=True):
            pass
        processed.export(out_path, format="s16le")
        return Path(out_path)
