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
    
    # if isinstance(results, str):
    #     return results
    # elif hasattr(results, 'output'):
    #     return results.output
    # else:
    #     return str(results)

    #
    structured_output = {}

    # If Crew returns a dict-like object, try extracting individual task results
    if isinstance(results, dict):
        for i, (task_name, result) in enumerate(results.items()):
            structured_output[f"Task {i+1}"] = {
                "agent": task_name,
                "output": result.raw_output if hasattr(result, "raw_output") else str(result)
            }
    elif isinstance(results, str):
        structured_output["result"] = results
    elif hasattr(results, 'output'):
        structured_output["result"] = results.output
    else:
        structured_output["result"] = str(results)

    return structured_output
    #

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
