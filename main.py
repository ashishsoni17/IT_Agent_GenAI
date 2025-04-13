# import os
# from crewai import Agent, Task, Crew, LLM
# import argparse
# import json
# from dotenv import load_dotenv
# import logging

# # Load environment variables from .env file
# load_dotenv()

# # Set up logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# def setup_llm():
#     """Initialize the language model based on environment variables"""
#     api_key = os.environ.get("GOOGLE_API_KEY")

#     if not api_key:
#         logging.error("GOOGLE_API_KEY environment variable not set")
#         print("Error: Please set your GOOGLE_API_KEY environment variable.")
#         print("Get an API key from https://aistudio.google.com/app/apikey")
#         exit(1)

#     try:
#         return LLM(
#             model="gemini/gemini-1.5-pro-latest",
#             temperature=0.7,
#             api_key=api_key
#         )
#     except Exception as e:
#         logging.error(f"Error initializing LLM: {e}")
#         print(f"Failed to initialize Gemini: {e}")
#         exit(1)

# def create_business_analyst_agent(llm):
#     return Agent(
#         role="Business Analyst",
#         goal="Understand requirements and translate them into technical insights",
#         backstory="""You are a senior business analyst with a keen ability to break down 
#         user needs and business goals into actionable technical requirements.""",
#         verbose=True,
#         llm=llm
#     )

# def create_designer_agent(llm):
#     return Agent(
#         role="UI/UX Designer",
#         goal="Design user-friendly and aesthetically pleasing interfaces",
#         backstory="""You are an expert UI/UX designer who creates intuitive user interfaces, 
#         wireframes, and visual layouts aligned with business and user needs.""",
#         verbose=True,
#         llm=llm
#     )

# def create_developer_agent(llm):
#     return Agent(
#         role="Software Developer",
#         goal="Develop robust and efficient software solutions",
#         backstory="""You write high-quality, maintainable code using best practices 
#         across multiple programming languages and frameworks.""",
#         verbose=True,
#         llm=llm
#     )

# def create_tester_agent(llm):
#     return Agent(
#         role="QA Tester",
#         goal="Ensure software quality by writing test cases and identifying bugs",
#         backstory="""You are a QA specialist skilled in writing test plans, automating tests, 
#         and identifying software issues before deployment.""",
#         verbose=True,
#         llm=llm
#     )

# def solve_problem(problem_description, agents_to_use=["business_analyst"]):
#     llm = setup_llm()

#     available_agents = {
#         "business_analyst": create_business_analyst_agent(llm),
#         "designer": create_designer_agent(llm),
#         "developer": create_developer_agent(llm),
#         "tester": create_tester_agent(llm)
#     }

#     active_agents = [available_agents[agent] for agent in agents_to_use if agent in available_agents]

#     if not active_agents:
#         logging.error("No valid agents selected")
#         return "Error: No valid agents were selected for this task."

#     tasks = []

#     if "business_analyst" in agents_to_use:
#         tasks.append(Task(
#             description=f"""Analyze the problem: {problem_description}
#             Break it down into key requirements and outline what the product should achieve.""",
#             agent=available_agents["business_analyst"],
#             expected_output="Requirements analysis and user needs"
#         ))

#     if "designer" in agents_to_use:
#         tasks.append(Task(
#             description=f"""Design a user interface or experience flow for the problem described: {problem_description}""",
#             agent=available_agents["designer"],
#             expected_output="UI/UX design plan or wireframes"
#         ))

#     if "developer" in agents_to_use:
#         tasks.append(Task(
#             description=f"""Write the software/code solution for the following problem: {problem_description}""",
#             agent=available_agents["developer"],
#             expected_output="Code implementation with explanation"
#         ))

#     if "tester" in agents_to_use:
#         tasks.append(Task(
#             description=f"""Develop test cases and identify edge cases and bugs for the problem described: {problem_description}""",
#             agent=available_agents["tester"],
#             expected_output="Test plan and bug analysis"
#         ))

#     crew = Crew(
#         agents=active_agents,
#         tasks=tasks,
#         verbose=True
#     )

#     results = crew.kickoff()

#     if isinstance(results, str):
#         return results
#     elif hasattr(results, 'output'):
#         return results.output
#     else:
#         return str(results)

# def chatbot_interface():
#     print("\n===== IT Project Simulation Agent =====")
#     print("Describe your technical problem, and I'll simulate the roles for you.")
#     print("Type 'exit' to quit the chat.")

#     global selected_agents
#     selected_agents = ["business_analyst"]

#     while True:
#         user_input = input("\nYou: ").strip()

#         if user_input.lower() == "exit":
#             print("Goodbye!")
#             break

#         if user_input.lower() == "help":
#             print("\nCommands:")
#             print("  help     - Show this help message")
#             print("  exit     - Exit the chat")
#             print("  ba       - Use Business Analyst")
#             print("  designer - Use Designer")
#             print("  dev      - Use Developer")
#             print("  test     - Use Tester")
#             print("  all      - Use all agents")
#             continue

#         if user_input.lower() in ["ba", "designer", "dev", "test", "all"]:
#             agent_map = {
#                 "ba": ["business_analyst"],
#                 "designer": ["designer"],
#                 "dev": ["developer"],
#                 "test": ["tester"],
#                 "all": ["business_analyst", "designer", "developer", "tester"]
#             }
#             selected_agents = agent_map[user_input.lower()]
#             print(f"Selected {', '.join(selected_agents)} agent(s) for next problem.")
#             continue

#         print("\nSimulating project... (this may take a moment)")
#         solution = solve_problem(user_input, selected_agents)
#         print("\nProject Output:")
#         print(solution)

#         selected_agents = ["business_analyst"]

# def main():
#     parser = argparse.ArgumentParser(description="IT Project Simulation Agent")
#     parser.add_argument('--problem', type=str, help="Problem to solve (runs in non-interactive mode)")
#     parser.add_argument('--agents', type=str, default="business_analyst", help="Agents to use: 'ba', 'designer', 'dev', 'test', or 'all'")
#     args = parser.parse_args()

#     agent_map = {
#         "ba": ["business_analyst"],
#         "designer": ["designer"],
#         "dev": ["developer"],
#         "test": ["tester"],
#         "all": ["business_analyst", "designer", "developer", "tester"]
#     }

#     if args.problem:
#         selected_agents = agent_map.get(args.agents.lower(), ["business_analyst"])
#         solution = solve_problem(args.problem, selected_agents)
#         print(solution)
#     else:
#         chatbot_interface()

# if __name__ == "__main__":
#     main()





import os
import argparse
import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def setup_llm():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logging.error("GOOGLE_API_KEY is not set in environment variables.")
        print("Set GOOGLE_API_KEY in .env file or environment variables.")
        exit(1)

    try:
        return LLM(
            model="gemini/gemini-1.5-pro-latest",
            temperature=0.7,
            api_key=api_key
        )
    except Exception as e:
        logging.error(f"LLM initialization failed: {e}")
        exit(1)

def create_agents(llm):
    return {
        "business_analyst": Agent(
            role="Business Analyst",
            goal="Understand requirements and translate them into technical insights",
            backstory="Senior BA skilled at analyzing user needs and business goals.",
            verbose=True,
            llm=llm
        ),
        "designer": Agent(
            role="UI/UX Designer",
            goal="Design user-friendly and aesthetic interfaces",
            backstory="Expert UI/UX designer with experience in user flows and wireframes.",
            verbose=True,
            llm=llm
        ),
        "developer": Agent(
            role="Software Developer",
            goal="Write efficient, maintainable code",
            backstory="Developer proficient in multi-language programming and best practices.",
            verbose=True,
            llm=llm
        ),
        "tester": Agent(
            role="QA Tester",
            goal="Write test plans and identify bugs",
            backstory="Quality assurance specialist with strong test automation skills.",
            verbose=True,
            llm=llm
        )
    }

def generate_tasks(problem_description, agents, selected_roles):
    task_templates = {
        "business_analyst": Task(
            description=f"Analyze and extract requirements for: {problem_description}",
            agent=agents["business_analyst"],
            expected_output="Requirements analysis and user needs"
        ),
        "designer": Task(
            description=f"Design UI/UX flow for: {problem_description}",
            agent=agents["designer"],
            expected_output="UI/UX design plan or wireframes"
        ),
        "developer": Task(
            description=f"Implement a solution for: {problem_description}",
            agent=agents["developer"],
            expected_output="Code implementation with explanation"
        ),
        "tester": Task(
            description=f"Create test cases and identify bugs for: {problem_description}",
            agent=agents["tester"],
            expected_output="Test plan and bug analysis"
        )
    }

    return [task_templates[role] for role in selected_roles if role in agents]

def solve_problem(problem_description, selected_roles):
    llm = setup_llm()
    agents = create_agents(llm)

    selected_agents = [agents[role] for role in selected_roles if role in agents]
    if not selected_agents:
        return "⚠️ Error: No valid agents selected."

    tasks = generate_tasks(problem_description, agents, selected_roles)

    crew = Crew(agents=selected_agents, tasks=tasks, verbose=True)
    result = crew.kickoff()

    if hasattr(result, 'output'):
        return result.output
    return result if isinstance(result, str) else str(result)

def chatbot_interface():
    print("\n===== IT Project Simulation Agent =====")
    print("Type your IT problem and watch agents collaborate!")
    print("Type 'exit' to quit, or 'help' for commands.")

    selected_agents = ["business_analyst"]

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break
        elif user_input.lower() == "help":
            print("\nCommands:\n  help - Show commands\n  exit - Quit\n  ba/designer/dev/test/all")
            continue
        elif user_input.lower() in ["ba", "designer", "dev", "test", "all"]:
            role_map = {
                "ba": ["business_analyst"],
                "designer": ["designer"],
                "dev": ["developer"],
                "test": ["tester"],
                "all": ["business_analyst", "designer", "developer", "tester"]
            }
            selected_agents = role_map[user_input.lower()]
            print(f"✅ Selected agents: {', '.join(selected_agents)}")
            continue

        print("\n💼 Simulating project...")
        output = solve_problem(user_input, selected_agents)
        print("\n🔍 Output:\n", output)

        selected_agents = ["business_analyst"]

def main():
    parser = argparse.ArgumentParser(description="IT Project Simulation Agent")
    parser.add_argument('--problem', type=str, help="Provide a problem to run in non-interactive mode")
    parser.add_argument('--agents', type=str, default="ba", help="Agent group: ba/designer/dev/test/all")
    args = parser.parse_args()

    role_map = {
        "ba": ["business_analyst"],
        "designer": ["designer"],
        "dev": ["developer"],
        "test": ["tester"],
        "all": ["business_analyst", "designer", "developer", "tester"]
    }

    if args.problem:
        selected_roles = role_map.get(args.agents.lower(), ["business_analyst"])
        result = solve_problem(args.problem, selected_roles)
        print(result)
    else:
        chatbot_interface()

if __name__ == "__main__":
    main()


