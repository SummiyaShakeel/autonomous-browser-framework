import logging
from src.browser_engine import BrowserEngine
from src.human_behavior import HumanBehaviorEngine
from src.tools import TOOL_REGISTRY

# Set up dedicated Agent logger
logger = logging.getLogger("AgentLogger")
logger.setLevel(logging.INFO)


class AgentState:
    IDLE = "IDLE"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
    FINISHED = "FINISHED"


class AutonomousAgent:
    def __init__(self, name="Agent_Alpha", browser_type="chromium", headless=False, profile_name=None):
        """Initializes Agent attributes, configurations, and lifecycle registers."""
        self.name = name
        self.browser_type = browser_type
        self.headless = headless
        # Stateful Profile Memory Name linking
        self.profile_name = profile_name if profile_name else f"{name.lower()}_session"

        self.state = AgentState.IDLE
        self.engine = None
        self.human = None
        self.history = []  # Structured log tracking inside the agent

        self._log_event(f"Agent '{self.name}' initialized in {self.state} state.")

    def _log_event(self, message, level="INFO"):
        """Maintains structural log records and tracks runtime history internally."""
        formatted_msg = f"[{self.name}] - {message}"
        self.history.append(
            {"time": logger.handlers[0].formatter if logger.handlers else "", "msg": message, "level": level})
        if level == "INFO":
            logger.info(formatted_msg)
        elif level == "WARNING":
            logger.warning(formatted_msg)
        elif level == "ERROR":
            logger.error(formatted_msg)

    def transition_to(self, target_state):
        """Implements a strict State Machine transition tracker."""
        self._log_event(f"State transitioning: {self.state} -> {target_state}")
        self.state = target_state

    # ==========================================
    # AGENT WORKFLOW & PIPELINE EXECUTION
    # ==========================================
    def startup(self):
        """Executes initialization sequence: configuration loads, starts browser engine and memory context."""
        self.transition_to(AgentState.STARTING)
        try:
            self.engine = BrowserEngine()
            # Override configurations using agent parameters
            self.engine.config.BROWSER_TYPE = self.browser_type
            self.engine.config.HEADLESS = self.headless

            # Start persistent user context
            page = self.engine.start(profile_name=self.profile_name)
            self.human = HumanBehaviorEngine(page)

            self.transition_to(AgentState.RUNNING)
            self._log_event("Execution engine, behavioral modules, and storage profiles activated.")
        except Exception as e:
            self.transition_to(AgentState.ERROR)
            self._log_event(f"Failed to start Agent pipeline: {e}", "ERROR")
            self.shutdown()
            raise

    def use_tool(self, tool_name, **kwargs):
        """Routes execution commands dynamically to our structured Tool System."""
        if self.state != AgentState.RUNNING:
            self._log_event(f"Cannot execute tool {tool_name} while in state: {self.state}", "WARNING")
            return None

        if tool_name not in TOOL_REGISTRY:
            self._log_event(f"Tool {tool_name} not found in global register.", "WARNING")
            return None

        tool = TOOL_REGISTRY[tool_name]
        self._log_event(f"Executing tool: {tool_name}")

        try:
            # Provide current engine context and behavior layers dynamically to the executing tool
            result = tool.execute(self.engine, human_behavior=self.human, **kwargs)
            self._log_event(f"Tool {tool_name} execution success: {result}")
            return result
        except Exception as e:
            self._log_event(f"Tool {tool_name} failed execution. Details: {e}", "ERROR")
            self.transition_to(AgentState.ERROR)
            raise

    def shutdown(self):
        """Handles graceful system teardown, resource release, and profiles saving."""
        self._log_event("Initiating graceful shutdown sequence...")
        try:
            if self.engine:
                self.engine.close()
            self.transition_to(AgentState.FINISHED)
            self._log_event("Shutdown operations terminated safely.")
        except Exception as e:
            self.transition_to(AgentState.ERROR)
            self._log_event(f"Error encountered during agent teardown: {e}", "ERROR")