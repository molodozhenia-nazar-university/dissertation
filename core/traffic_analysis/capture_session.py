import os
import time
from scapy.all import AsyncSniffer, PcapWriter
from threading import Thread, Event


class CaptureSession:

    def __init__(
        self,
        interface,
        use_duration,
        duration,
        buffer_spin_mb,
        output_path,
        update_result_text,
        on_finished,
    ):
        self.interface = interface
        self.use_duration = use_duration
        self.duration = duration
        self.maximum_size_file_mb = buffer_spin_mb
        self.output_path = output_path
        self.update_result_text = update_result_text
        self.on_finished = on_finished

        self.stop_event = Event()
        self.sniffer = None
        self.writer = None

        self.start_time = None
        self.end_time = None
        self.packet_counter = 0

    def start(self):

        try:

            self.update_result_text(f'🔍 Початок захоплення з "{self.interface}"')

            self.writer = PcapWriter(self.output_path, append=False, sync=True)

            # Information - use duration and duration
            if self.use_duration and self.duration > 0:
                self.update_result_text(f"🕒 Тривалість: максимум {self.duration} сек")
            else:
                self.update_result_text("🕒 Тривалість: до ручної зупинки")

            # Information - size file
            self.maximum_size_file_bytes = None
            if self.maximum_size_file_mb is not None and self.maximum_size_file_mb > 0:
                self.maximum_size_file_bytes = self.maximum_size_file_mb * 1024 * 1024
                self.update_result_text(
                    f"📦 Максимальний розмір файлу: ~{self.maximum_size_file_mb} МБ"
                )

            self.sniffer = AsyncSniffer(
                iface=self.interface,
                prn=self._packet_callback,
                store=False,
            )

            self.sniffer.start()

            self.start_time = time.time()

            Thread(target=self._watcher_thread, daemon=True).start()

        except Exception as e:
            self.update_result_text(f"❌ Помилка захоплення: {e}")
            self._safe_finish()

    def _packet_callback(self, packet):

        if self.stop_event.is_set():
            return

        if self.writer is not None:

            self.writer.write(packet)
            self.packet_counter += 1

            if self.maximum_size_file_bytes is not None:
                try:

                    current_size = os.path.getsize(self.output_path)
                    if current_size >= self.maximum_size_file_bytes:
                        self.update_result_text(
                            "\n🟡 Досягнуто максимальний розмір файлу — зупинка запису трафіку\n"
                        )
                        self.stop_event.set()
                        return

                except OSError:
                    pass

    def _watcher_thread(self):

        while not self.stop_event.is_set():
            if self.use_duration and self.duration > 0 and self.start_time is not None:
                elapsed = time.time() - self.start_time
                if elapsed >= self.duration:
                    self.update_result_text(
                        "\n🟡 Час моніторингу вичерпано — зупинка запису трафіку\n"
                    )
                    self.stop_event.set()
                    break
            time.sleep(0.1)

        self._finish()  # Active for _packet_callback() and stop()

    def stop(self):

        if self.stop_event.is_set():
            return

        self.update_result_text("\n🟡 Зупинка запису трафіку\n")
        self.stop_event.set()

    def _finish(self):

        self.end_time = time.time()

        elapsed = None

        if self.start_time is not None:
            elapsed = self.end_time - self.start_time

        try:

            if self.sniffer is not None:
                self.sniffer.stop()

            if self.writer is not None:
                self.writer.close()
                self.writer = None

            try:

                file_size_bytes = os.path.getsize(self.output_path)
                file_size_mb = file_size_bytes / (1024 * 1024)

            except OSError:

                file_size_bytes = None
                file_size_mb = None

            self.update_result_text("🔴 Моніторинг завершено\n")

            if elapsed is not None:
                self.update_result_text(f"⏱ Фактична тривалість: {elapsed:.1f} сек")

            if file_size_mb is not None:
                self.update_result_text(
                    f"📦 Розмір файлу: {file_size_mb:.2f} МБ "
                    f"({file_size_bytes} байт)"
                )

            self.update_result_text(f"➕ Захоплено пакетів: {self.packet_counter}")
            self.update_result_text(f"📁 Файл збережено: {self.output_path}")

        except Exception as e:
            self.update_result_text(f"❌ Помилка захоплення: {e}")

        if self.on_finished is not None:
            try:
                self.on_finished()
            except Exception:
                pass

    def _safe_finish(self):

        try:
            if self.sniffer is not None:
                self.sniffer.stop()
            if self.writer is not None:
                self.writer.close()
                self.writer = None
        except Exception:
            pass

        if self.on_finished is not None:
            try:
                self.on_finished()
            except Exception:
                pass
