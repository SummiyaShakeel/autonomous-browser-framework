import time
import logging
import concurrent.futures
from src.agent import AutonomousAgent, AgentState
from src.scheduler import Task, TaskState

logger = logging.getLogger("MultiAgentLogger")
logger.setLevel(logging.INFO)


class MultiAgentManager:
    def __init__(self):
        """Manages the pool registration, resource isolation, and task dispatching."""
        self.agent_pool = {}  # Map of agent_name -> AutonomousAgent[cite: 10]
        self.active_tasks = {}  # Tracks which agent is running which task[cite: 10]

    def register_agent(self, agent: AutonomousAgent):
        """Registers an initialized agent into our managed pool[cite: 10]."""
        self.agent_pool[agent.name] = agent
        logger.info(f"[Agent Manager] Successfully registered agent: {agent.name}[cite: 10]")

    def dispatch_task_to_agent(self, agent_name, task: Task):
        """Dispatches a task to an isolated, dedicated agent resource[cite: 10]."""
        agent = self.agent_pool.get(agent_name)
        if not agent:
            logger.error(f"[Agent Manager] Agent '{agent_name}' not found in pool[cite: 10].")
            return False

        if agent.state == AgentState.RUNNING or agent.state == AgentState.STARTING:
            logger.warning(f"[Agent Manager] Agent '{agent_name}' is currently busy[cite: 10].")
            return False

        logger.info(f"[Agent Manager] Dispatching '{task.name}' to isolated profile of '{agent_name}'[cite: 10].")
        self.active_tasks[agent_name] = task
        task.status = TaskState.RUNNING

        try:
            # Strict Resource Isolation[cite: 10]
            agent.startup()

            # Run the tool action[cite: 10]
            result = agent.use_tool(task.tool_name, **task.params)
            task.status = TaskState.COMPLETED
            logger.info(f"[Agent Manager] Agent '{agent_name}' completed task successfully[cite: 10]. Result: {result}")

            # --- 🌟 VISUAL INSPECTION DELAY ---
            # Hold both windows open for 5 seconds so you can watch them run concurrently!
            logger.info(f"[Agent Manager] Holding '{agent_name}' open for visual inspection...")
            time.sleep(5)

            return True

        except Exception as e:
            task.status = TaskState.FAILED
            task.error_message = str(e)
            logger.error(f"[Agent Manager] Agent '{agent_name}' failed during task execution: {e}[cite: 10]")
            return False

        finally:
            agent.shutdown()  # Terminate execution and close the isolated context cleanly[cite: 10]
            if agent_name in self.active_tasks:
                del self.active_tasks[agent_name]

    def run_parallel_tasks(self, task_assignments):
        """Executes multiple tasks across different agents concurrently[cite: 10]."""
        logger.info(
            f"[Agent Manager] Launching parallel execution across {len(task_assignments)} agent nodes...[cite: 10]")

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(task_assignments)) as executor:
            futures = []
            for assignment in task_assignments:
                name = assignment["agent_name"]
                task = assignment["task"]
                futures.append(
                    executor.submit(self.dispatch_task_to_agent, name, task)
                )

            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            logger.info(f"[Agent Manager] Parallel swarm operations completed. Results: {results}[cite: 10]")