import time
import logging
from src.agent import AutonomousAgent
from src.ai_decision_engine import AIDecisionEngine
from src.monitor import ProductionMonitor  # Module 10 Monitor[cite: 1]

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_production_pipeline():
    logging.info("--- Starting Production-Grade Autonomous execution ---")
    agent = AutonomousAgent(
        name="Production_Agent",
        browser_type="chromium",
        headless=False,  # Change this to False so you can see the browser window!
        profile_name="production_session"
    )

    ai_engine = AIDecisionEngine()

    try:
        # Measure system resource performance before launch[cite: 1]
        ProductionMonitor.log_system_metrics()

        # Profile execution runtime logic utilizing our wrapper tool[cite: 1]
        ProductionMonitor.measure_execution_time(agent.startup)

        objective = "Go to google.com and search for AI Multi-Agent Swarms"

        # Execute goal
        ProductionMonitor.measure_execution_time(
            ai_engine.execute_autonomous_goal, agent, objective
        )

        # Log active resource states upon task completion[cite: 1]
        ProductionMonitor.log_system_metrics()

    except Exception as run_error:
        logging.critical(f"Production pipeline run fault: {run_error}")

    finally:
        agent.shutdown()
        logging.info("--- Production pipeline run finished ---")


if __name__ == "__main__":
    import os

    os.makedirs("outputs", exist_ok=True)
    run_production_pipeline()
