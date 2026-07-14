import logging
from src.llm_provider import MockLocalProvider

logger = logging.getLogger("AIDecisionEngine")


class AIDecisionEngine:
    def __init__(self, provider=None):
        """Initializes decision engine with prompt templates and dynamic planning structures[cite: 7]."""
        self.provider = provider if provider else MockLocalProvider()

        # System Prompt Setup (Module 9, Task 3 Prompt Management)[cite: 7]
        self.system_prompt_template = (
            "You are an Autonomous Browser Agent[cite: 7]. Your objective is to achieve the user's goal "
            "by executing a sequence of steps using the available tools[cite: 7]. "
            "You must generate an incremental execution plan, route parameters correctly, "
            "and reflect/self-correct if any tool execution fails[cite: 7]."
        )

    def formulate_plan(self, objective, available_tools):
        """Generates the sequential execution steps using the LLM Provider[cite: 7]."""
        user_prompt = f"Objective: {objective}\nAvailable Tools: {list(available_tools.keys())}[cite: 7]"

        logger.info(f"[AI Engine] Analyzing Objective: '{objective}'[cite: 7]")

        # Generate raw response mapping via abstract layer[cite: 7]
        response = self.provider.generate_response(self.system_prompt_template, user_prompt)

        logger.info(f"[AI Engine] Decided Thoughts: {response['thought']}[cite: 7]")
        return response["plan"]

    def execute_autonomous_goal(self, agent, objective):
        """Master Orchestrator: Runs the goal execution pipeline with active Reflection (Task 6)."""
        logger.info(f"[AI Engine] Launching Autonomous Work Loop for Agent: {agent.name}")

        from src.tools import TOOL_REGISTRY

        plan = self.formulate_plan(objective, TOOL_REGISTRY)

        for step_idx, step in enumerate(plan):
            tool_name = step["tool"]
            args = step["args"]

            success = False
            retries = 0
            max_reflection_attempts = 2

            while not success and retries <= max_reflection_attempts:
                try:
                    logger.info(f"[AI Engine] Running Plan Step {step_idx + 1}: Calling Tool '{tool_name}' with {args}")
                    agent.use_tool(tool_name, **args)
                    success = True
                except Exception as error:
                    retries += 1
                    logger.warning(
                        f"[AI Engine] [Reflection Triggered] Step '{tool_name}' failed: {error}. "
                        f"Reflecting on alternative strategy (Attempt {retries}/{max_reflection_attempts})..."
                    )

                    # 🌟 FIX: Reset Agent State to RUNNING so the state machine accepts the retry command
                    agent.transition_to("RUNNING")

                    if tool_name == "type_text" and "selector" in args:
                        logger.info("[Reflection] Correcting selector parameter to fallback inputs...")
                        args["selector"] = "input[type='text']"
                    else:
                        import time
                        time.sleep(2)

            if not success:
                logger.critical(f"[AI Engine] Plan failed at step {step_idx + 1}. Unrecoverable operational state.")
                break