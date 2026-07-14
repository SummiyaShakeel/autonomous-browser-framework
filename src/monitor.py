import time
import logging
import psutil  # To gather real-time host resource utilization metrics

logger = logging.getLogger("MonitorLogger")
logger.setLevel(logging.INFO)


class ProductionMonitor:
    @staticmethod
    def log_system_metrics():
        """Captures host system CPU, memory, and active processes (Module 10, Task 2)."""
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()

        logger.info(
            f"[Monitor] System Metrics Summary -> "
            f"CPU Utilization: {cpu_usage}% | "
            f"RAM Usage: {memory_info.percent}% ({memory_info.used / (1024 ** 2):.1f}MB Used)"
        )
        return {
            "cpu_percent": cpu_usage,
            "memory_percent": memory_info.percent
        }

    @staticmethod
    def measure_execution_time(func, *args, **kwargs):
        """Wrapper utility to measure performance throughput and trace bottlenecks."""
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        logger.info(f"[Monitor] Profile Trace -> Execution '{func.__name__}' took {duration:.3f} seconds.")
        return result