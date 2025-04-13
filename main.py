import os
from crewai import Agent, Task, Crew, LLM
import argparse
import json
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_llm():
    """Initialize the language model based on environment variables"""
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        logging.error("GOOGLE_API_KEY environment variable not set")
        print("Error: Please set your GOOGLE_API_KEY environment variable.")
        print("Get an API key from https://aistudio.google.com/app/apikey")
        exit(1)
        
    try:
        return LLM(
            model="gemini/gemini-1.5-pro-latest",
            temperature=0.7,
            api_key=api_key
        )
    except Exception as e:
        logging.error(f"Error initializing LLM: {e}")
        print(f"Failed to initialize Gemini: {e}")
        exit(1)

def create_it_agent(llm):
    """Create the IT problem-solving agent"""
    return Agent(
        role="IT Solutions Specialist",
        goal="Solve technical problems and provide practical solutions",
        backstory="""You are an experienced IT specialist with expertise in 
        software development, networking, cybersecurity, and system administration.
        You have 15 years of experience solving complex technical problems and
        providing clear, actionable solutions.""",
        verbose=True,
        llm=llm
    )

def create_coding_agent(llm):
    """Create specialized coding agent"""
    return Agent(
        role="Software Developer",
        goal="Write clean, efficient code to solve programming problems",
        backstory="""You are a senior software developer with expertise in multiple
        programming languages including Python, JavaScript, Java, and C++. You can
        develop algorithms, debug code, and implement software solutions.""",
        verbose=True,
        llm=llm
    )

def solve_problem(problem_description, agents_to_use=["it"]):
    """Solve a given technical problem using appropriate agents"""
    llm = setup_llm()
    
    # Initialize agents
    available_agents = {
        "it": create_it_agent(llm),
        "coder": create_coding_agent(llm)
    }
    
    # Select agents to use
    active_agents = [available_agents[agent] for agent in agents_to_use if agent in available_agents]
    
    if not active_agents:
        logging.error("No valid agents selected")
        return "Error: No valid agents were selected for this task."
    
    # Create tasks
    tasks = []
    
    if "it" in agents_to_use:
        tasks.append(Task(
            description=f"""
            Analyze the following technical problem:
            
            {problem_description}
            
            Provide a comprehensive solution including:
            1. Root cause analysis
            2. Step-by-step resolution process
            3. Preventive measures for the future
            
            Be specific and practical in your approach.
            """,
            agent=available_agents["it"],
            expected_output="Detailed solution to the technical problem"
        ))
    
    if "coder" in agents_to_use:
        tasks.append(Task(
            description=f"""
            Write code to solve the following programming problem:
            
            {problem_description}
            
            Provide:
            1. Complete working code
            2. Explanation of the solution approach
            3. Documentation for usage
            4. Analysis of time and space complexity (if applicable)
            
            Make sure the code is well-structured, efficient, and follows best practices.
            """,
            agent=available_agents["coder"],
            expected_output="Complete code solution with documentation"
        ))
    
    # Create crew and run tasks
    # FIXED: Changed verbose=2 to verbose=True
    crew = Crew(
        agents=active_agents,
        tasks=tasks,
        verbose=True  # Changed from integer (2) to boolean (True)
    )
    
    results = crew.kickoff()
    
    # Combine and return results
    # combined_solution = ""
    # for task_name, result in results.items():
    #     combined_solution += f"\n\n{result.raw_output}"
    
    # 
    return results.output

def chatbot_interface():
    """Interactive chat interface for IT problem-solving"""
    print("\n===== IT Problem-Solving Agent =====")
    print("Describe your technical problem, and I'll solve it for you.")
    print("Type 'exit' to quit the chat.")
    
    # Initialize selected_agents global variable
    global selected_agents
    selected_agents = ["it"]
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
            
        if user_input.lower() == "help":
            print("\nCommands:")
            print("  help  - Show this help message")
            print("  exit  - Exit the chat")
            print("  code  - Use coding agent for next problem")
            print("  it    - Use IT agent for next problem (default)")
            print("  both  - Use both agents for next problem")
            continue
            
        if user_input.lower() in ["code", "it", "both"]:
            agent_map = {
                "code": ["coder"],
                "it": ["it"],
                "both": ["it", "coder"]
            }
            selected_agents
            selected_agents = agent_map[user_input.lower()]
            print(f"Selected {', '.join(selected_agents)} agent(s) for next problem.")
            continue
        
        print("\nSolving your problem... (this may take a moment)")
        solution = solve_problem(user_input, selected_agents)
        print("\nSolution:")
        print(solution)
        
        # Reset to default agent
        selected_agents = ["it"]

def main():
    parser = argparse.ArgumentParser(description="IT Problem-Solving Agent")
    parser.add_argument('--problem', type=str, help="Problem to solve (runs in non-interactive mode)")
    parser.add_argument('--agents', type=str, default="it", help="Agents to use: 'it', 'coder', or 'both'")
    args = parser.parse_args()
    
    agent_map = {
        "it": ["it"],
        "coder": ["coder"],
        "both": ["it", "coder"]
    }
    
    if args.problem:
        # Non-interactive mode
        selected_agents = agent_map.get(args.agents.lower(), ["it"])
        solution = solve_problem(args.problem, selected_agents)
        print(solution)
    else:
        # Interactive chat mode
        chatbot_interface()

if __name__ == "__main__":
    main()



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

# def create_it_agent(llm):
#     """Create the IT problem-solving agent"""
#     return Agent(
#         role="IT Solutions Specialist",
#         goal="Solve technical problems and provide practical solutions",
#         backstory="""You are an experienced IT specialist with expertise in 
#         software development, networking, cybersecurity, and system administration.
#         You have 15 years of experience solving complex technical problems and
#         providing clear, actionable solutions.""",
#         verbose=True,
#         llm=llm
#     )

# def create_coding_agent(llm):
#     """Create specialized coding agent"""
#     return Agent(
#         role="Software Developer",
#         goal="Write clean, efficient code to solve programming problems",
#         backstory="""You are a senior software developer with expertise in multiple
#         programming languages including Python, JavaScript, Java, and C++. You can
#         develop algorithms, debug code, and implement software solutions.""",
#         verbose=True,
#         llm=llm
#     )

# def solve_problem(problem_description, agents_to_use=["it"]):
#     """Solve a given technical problem using appropriate agents"""
#     llm = setup_llm()
    
#     # Initialize agents
#     available_agents = {
#         "it": create_it_agent(llm),
#         "coder": create_coding_agent(llm)
#     }
    
#     # Select agents to use
#     active_agents = [available_agents[agent] for agent in agents_to_use if agent in available_agents]
    
#     if not active_agents:
#         logging.error("No valid agents selected")
#         return "Error: No valid agents were selected for this task."
    
#     # Create tasks
#     tasks = []
    
#     if "it" in agents_to_use:
#         tasks.append(Task(
#             description=f"""
#             Analyze the following technical problem:
            
#             {problem_description}
            
#             Provide a comprehensive solution including:
#             1. Root cause analysis
#             2. Step-by-step resolution process
#             3. Preventive measures for the future
            
#             Be specific and practical in your approach.
#             """,
#             agent=available_agents["it"],
#             expected_output="Detailed solution to the technical problem"
#         ))
    
#     if "coder" in agents_to_use:
#         tasks.append(Task(
#             description=f"""
#             Write code to solve the following programming problem:
            
#             {problem_description}
            
#             Provide:
#             1. Complete working code
#             2. Explanation of the solution approach
#             3. Documentation for usage
#             4. Analysis of time and space complexity (if applicable)
            
#             Make sure the code is well-structured, efficient, and follows best practices.
#             """,
#             agent=available_agents["coder"],
#             expected_output="Complete code solution with documentation"
#         ))
    
#     # Create crew and run tasks
#     crew = Crew(
#         agents=active_agents,
#         tasks=tasks,
#         verbose=2
#     )
    
#     results = crew.kickoff()
    
#     # Combine and return results
#     combined_solution = ""
#     for task_name, result in results.items():
#         combined_solution += f"\n\n{result.raw_output}"
    
#     return combined_solution

# def chatbot_interface():
#     """Interactive chat interface for IT problem-solving"""
#     print("\n===== IT Problem-Solving Agent =====")
#     print("Describe your technical problem, and I'll solve it for you.")
#     print("Type 'exit' to quit the chat.")
    
#     while True:
#         user_input = input("\nYou: ").strip()
        
#         if user_input.lower() == "exit":
#             print("Goodbye!")
#             break
            
#         if user_input.lower() == "help":
#             print("\nCommands:")
#             print("  help  - Show this help message")
#             print("  exit  - Exit the chat")
#             print("  code  - Use coding agent for next problem")
#             print("  it    - Use IT agent for next problem (default)")
#             print("  both  - Use both agents for next problem")
#             continue
            
#         if user_input.lower() in ["code", "it", "both"]:
#             agent_map = {
#                 "code": ["coder"],
#                 "it": ["it"],
#                 "both": ["it", "coder"]
#             }
#             selected_agents = agent_map[user_input.lower()]
#             print(f"Selected {', '.join(selected_agents)} agent(s) for next problem.")
#             continue
        
#         # Default to IT agent unless changed by user
#         selected_agents = globals().get("selected_agents", ["it"])
        
#         print("\nSolving your problem... (this may take a moment)")
#         solution = solve_problem(user_input, selected_agents)
#         print("\nSolution:")
#         print(solution)
        
#         # Reset to default agent
#         globals()["selected_agents"] = ["it"]

# def main():
#     parser = argparse.ArgumentParser(description="IT Problem-Solving Agent")
#     parser.add_argument('--problem', type=str, help="Problem to solve (runs in non-interactive mode)")
#     parser.add_argument('--agents', type=str, default="it", help="Agents to use: 'it', 'coder', or 'both'")
#     args = parser.parse_args()
    
#     agent_map = {
#         "it": ["it"],
#         "coder": ["coder"],
#         "both": ["it", "coder"]
#     }
    
#     if args.problem:
#         # Non-interactive mode
#         selected_agents = agent_map.get(args.agents.lower(), ["it"])
#         solution = solve_problem(args.problem, selected_agents)
#         print(solution)
#     else:
#         # Interactive chat mode
#         chatbot_interface()

# if __name__ == "__main__":
#     main()

# # # main.py

# # from crewai import Agent, Task, Crew, LLM
# # from crewai.tasks import TaskOutput
# # import os
# # import argparse
# # import json
# # from utils.logger_config import setup_logger
# # import logging
# # import google.auth

# # # Set up paths
# # CONFIG_PATH = os.path.join("config", "config.json")
# # ARTIFACTS_DIR = os.path.join("artifacts")

# # def load_config():
# #     """Load configuration or create default if not found"""
# #     try:
# #         if not os.path.exists("config"):
# #             os.makedirs("config")
# #             logging.warning("Config directory created.")
            
# #         if not os.path.exists(CONFIG_PATH):
# #             default_config = {
# #                 "logging_level": "INFO",
# #                 "enable_chat": True,
# #                 "business_requirements": [
# #                     "Create a secure user authentication system with login/logout functionality",
# #                     "Implement an admin panel that allows user management",
# #                     "Develop a dashboard to display user activities"
# #                 ],
# #                 "llm": {
# #                     "type": "gemini",
# #                     "model": "gemini-1.5-pro-latest",
# #                     "temperature": 0.7
# #                 }
# #             }
# #             with open(CONFIG_PATH, 'w') as file:
# #                 json.dump(default_config, file, indent=4)
# #             logging.info("Default config file created.")
# #             return default_config
            
# #         with open(CONFIG_PATH, 'r') as file:
# #             return json.load(file)
# #     except Exception as e:
# #         logging.error(f"Error loading config: {e}")
# #         return {"logging_level": "INFO", "enable_chat": True}

# # def load_template(template_name):
# #     """Load a template file from templates directory"""
# #     try:
# #         template_path = os.path.join("templates", f"{template_name}.txt")
# #         with open(template_path, 'r') as file:
# #             return file.read()
# #     except FileNotFoundError:
# #         logging.warning(f"Template {template_name} not found.")
# #         return ""

# # def save_artifact(artifact_name, content):
# #     """Save generated artifacts to the artifacts directory"""
# #     if not os.path.exists(ARTIFACTS_DIR):
# #         os.makedirs(ARTIFACTS_DIR)
    
# #     artifact_path = os.path.join(ARTIFACTS_DIR, f"{artifact_name}.txt")
# #     with open(artifact_path, 'w') as file:
# #         file.write(content)
# #     logging.info(f"Artifact saved: {artifact_path}")

# # def initialize_llm(config):
# #     """Initialize the language model based on configuration"""
# #     llm_config = config.get("llm", {"type": "gemini", "model": "gemini-1.5-pro-latest", "temperature": 0.7})
    
# #     if llm_config["type"] == "gemini":
# #         try:
# #             # For Google authentication
# #             # Option 1: If using application default credentials
# #             credentials, project = google.auth.default()
            
# #             # Option 2: Or if you have a service account key file
# #             # Replace with path to your service account key if available
# #             service_account_key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            
# #             return LLM(
# #                 model=f"gemini/{llm_config['model']}",
# #                 temperature=llm_config.get("temperature", 0.7),
# #                 api_key=os.environ.get("GOOGLE_API_KEY", None)  # If using API key approach
# #             )
# #         except Exception as e:
# #             logging.error(f"Error initializing Gemini: {e}")
# #             logging.warning("Make sure you have set up Google credentials properly.")
# #             raise
# #     else:
# #         logging.warning("Unsupported LLM type. Please use 'gemini' as the LLM type.")
# #         raise ValueError("Unsupported LLM type")

# # def run_project_simulation(config):
# #     """Run the full project simulation with crewAI"""
# #     # Initialize the LLM
# #     try:
# #         llm = initialize_llm(config)
# #     except Exception as e:
# #         logging.error(f"Failed to initialize LLM: {e}")
# #         logging.error("Please ensure Google credentials are properly set up")
# #         return {}
    
# #     # Load templates
# #     user_story_template = load_template("user_story_template")
# #     design_template = load_template("design_template")
# #     code_template = load_template("code_template")
# #     test_case_template = load_template("test_case_template")
    
# #     # Create the agents
# #     business_analyst = Agent(
# #         role="Business Analyst",
# #         goal="Transform business requirements into clear user stories for the development team",
# #         backstory="You have 10 years of experience in business analysis and requirements gathering. You're known for your ability to translate client needs into actionable stories.",
# #         verbose=True,
# #         llm=llm
# #     )
    
# #     designer = Agent(
# #         role="System Designer",
# #         goal="Create a coherent system design based on user stories",
# #         backstory="You have extensive experience in software architecture and system design, specializing in creating robust, scalable software solutions.",
# #         verbose=True,
# #         llm=llm
# #     )
    
# #     developer = Agent(
# #         role="Software Developer",
# #         goal="Implement working code that meets the requirements and follows the design",
# #         backstory="You're a senior developer with expertise in multiple programming languages. You write clean, maintainable code that follows best practices.",
# #         verbose=True,
# #         llm=llm
# #     )
    
# #     tester = Agent(
# #         role="QA Tester",
# #         goal="Ensure the software meets quality standards through thorough testing",
# #         backstory="You have a keen eye for detail and extensive experience in testing software applications. You always find edge cases others miss.",
# #         verbose=True,
# #         llm=llm
# #     )
    
# #     # Define the tasks
# #     create_user_stories = Task(
# #         description=f"""
# #         Analyze the following business requirements and create detailed user stories:
# #         {config.get('business_requirements', [])}
        
# #         Use this template for creating user stories:
# #         {user_story_template}
        
# #         Be thorough and think about all aspects of the system.
# #         """,
# #         agent=business_analyst,
# #         expected_output="Comprehensive list of user stories based on the business requirements"
# #     )
    
# #     create_design = Task(
# #         description="""
# #         Based on the user stories provided, create a detailed system design that includes:
# #         1. Component diagram
# #         2. Data models
# #         3. API specifications
# #         4. Technology stack recommendations
        
# #         Use this template for your design:
# #         {design_template}
        
# #         Consider scalability, security, and maintainability in your design.
# #         """,
# #         agent=designer,
# #         expected_output="Complete system design document",
# #         context=[create_user_stories]
# #     )
    
# #     generate_code = Task(
# #         description="""
# #         Implement the code based on the user stories and system design.
# #         Focus on the core functionality described in the requirements.
# #         Write clean, well-documented code.
        
# #         Use this template for code structure:
# #         {code_template}
# #         """,
# #         agent=developer,
# #         expected_output="Working code implementation",
# #         context=[create_user_stories, create_design]
# #     )
    
# #     create_tests = Task(
# #         description="""
# #         Create comprehensive test cases for the implemented code.
# #         Include both unit tests and integration tests.
# #         Consider edge cases and error scenarios.
        
# #         Use this template for test cases:
# #         {test_case_template}
        
# #         Execute the tests and report on their status.
# #         """,
# #         agent=tester,
# #         expected_output="Test cases and execution results",
# #         context=[create_user_stories, create_design, generate_code]
# #     )
    
# #     # Create the crew
# #     project_crew = Crew(
# #         agents=[business_analyst, designer, developer, tester],
# #         tasks=[create_user_stories, create_design, generate_code, create_tests],
# #         verbose=2
# #     )
    
# #     # Run the crew
# #     results = project_crew.kickoff()
    
# #     # Save artifacts
# #     for task, result in results.items():
# #         if isinstance(result, TaskOutput):
# #             artifact_name = task.name.lower().replace(" ", "_")
# #             save_artifact(artifact_name, result.raw_output)
    
# #     return results

# # def chat_with_pm(artifacts):
# #     """Simple chat interface for the Project Manager"""
# #     print("\n==== PROJECT MANAGER INTERFACE ====")
# #     print("Hello Project Manager! You can ask about any project artifact.")
# #     print("Available commands: user_stories, design, code, tests, exit")
    
# #     while True:
# #         query = input("\nPM> ").strip().lower()
        
# #         if query == "exit":
# #             print("Goodbye!")
# #             break
        
# #         artifact_map = {
# #             "user_stories": "create_user_stories",
# #             "design": "create_design",
# #             "code": "generate_code",
# #             "tests": "create_tests"
# #         }
        
# #         if query in artifact_map:
# #             task_name = artifact_map[query]
# #             if task_name in artifacts:
# #                 result = artifacts[task_name]
# #                 if isinstance(result, TaskOutput):
# #                     print(f"\n=== {query.upper()} ===\n")
# #                     print(result.raw_output)
# #                 else:
# #                     print(f"Found {query}, but the output format is unexpected.")
# #             else:
# #                 print(f"No {query} artifact found.")
# #         else:
# #             print("Unknown command. Available commands: user_stories, design, code, tests, exit")

# # def main():
# #     parser = argparse.ArgumentParser(description="Simulate IT Project Lifecycle with crewAI")
# #     parser.add_argument('--no-chat', action='store_true', help="Run simulation without PM bot interaction")
# #     args = parser.parse_args()
    
# #     config = load_config()
# #     setup_logger(level=config.get("logging_level", "INFO"))
    
# #     logging.info("Starting Project Simulation...")
# #     artifacts = run_project_simulation(config)
# #     logging.info("Project Simulation Completed.")
    
# #     if not args.no_chat and config.get("enable_chat", True):
# #         chat_with_pm(artifacts)

# # if __name__ == "__main__":
# #     main()