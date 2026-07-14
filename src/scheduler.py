import time
import uuid
import logging
import queue

# Set up logging for scheduler operations
logger = logging.getLogger("SchedulerLogger")
logger.setLevel(logging.INFO)


class TaskState:
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


class Task:
    def __init__(self, name, tool_name, params=None, priority=1, max_retries=3):
        """Represents the basic unit of work inside the framework."""
        self.task_id = str(uuid.uuid4())[:8]
        self.name = name
        self.tool_name = tool_name
        self.params = params if params else {}
        self.priority = priority  # Lower number = Higher priority (e.g., 1 is higher than 3)
        self.status = TaskState.PENDING
        self.max_retries = max_retries
        self.retry_count = 0
        self.error_message = None

    def __lt__(self, other):
        """Enables Python's PriorityQueue to compare tasks based on their priority value."""
        return self.priority < other.priority


class Workflow:
    def __init__(self, name):
        """Encapsulates a sequential chain of tasks."""
        self.name = name
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)


class TaskScheduler:
    def __init__(self, agent):
        """Manages queueing, time-based execution delays, and error recovery."""
        self.agent = agent
        # Use Python's thread-safe PriorityQueue
        self.task_queue = queue.PriorityQueue()
        self.completed_tasks = []
        self.failed_tasks = []

    def add_task_to_queue(self, task: Task):
        """Pushes a task into the prioritized execution queue."""
        task.status = TaskState.PENDING
        self.task_queue.put(task)
        logger.info(f"[Scheduler] Task queued: {task.name} (Priority: {task.priority})")

    def add_workflow_to_queue(self, workflow: Workflow):
        """Enqueues an entire sequential workflow chain."""
        logger.info(f"[Scheduler] Enqueueing sequential workflow: {workflow.name}")
        for task in workflow.tasks:
            self.add_task_to_queue(task)

    def run_next_task(self):
        """Pulls and executes the highest priority task currently in the queue."""
        if self.task_queue.empty():
            logger.info("[Scheduler] Task queue is empty.")
            return False

        task = self.task_queue.get()
        task.status = TaskState.RUNNING
        logger.info(f"[Scheduler] Executing task: {task.name} using Tool: {task.tool_name}")

        try:
            # Route the execution to our agent's Tool System
            result = self.agent.use_tool(task.tool_name, **task.params)
            task.status = TaskState.COMPLETED
            self.completed_tasks.append(task)
            logger.info(f"[Scheduler] Task completed successfully: {task.name}")
            return True

        except Exception as e:
            task.error_message = str(e)
            logger.error(f"[Scheduler] Error executing task '{task.name}': {e}")

            # Handle Retry and Fault Tolerance Logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskState.RETRYING
                logger.warning(
                    f"[Scheduler] Retrying task '{task.name}' ({task.retry_count}/{task.max_retries}) after a short delay...")
                time.sleep(2)  # Delay before retrying
                self.task_queue.put(task)  # Re-enqueue
            else:
                task.status = TaskState.FAILED
                self.failed_tasks.append(task)
                logger.critical(f"[Scheduler] Task '{task.name}' has failed permanently after reaching max retries.")

            return False

    def run_all(self):
        """Executes all queued tasks until the priority queue is exhausted."""
        logger.info("[Scheduler] Starting scheduler processing loop...")
        while not self.task_queue.empty():
            self.run_next_task()
        logger.info("[Scheduler] Processing cycle complete.")