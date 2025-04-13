
import streamlit as st
from main import solve_problem

# Streamlit app title
st.set_page_config(page_title="IT Agent Assistant", layout="wide")
st.title("🧠 IT Agent - AI Technical Problem Solver")

# Input area
problem = st.text_area("Describe your technical problem below:", height=200)

# Agent selection
agent_option = st.radio(
    "Which agent(s) would you like to use?",
    ("IT Agent", "Coder Agent", "Both")
)

# Map selection
agent_map = {
    "IT Agent": ["it"],
    "Coder Agent": ["coder"],
    "Both": ["it", "coder"]
}

selected_agents = agent_map[agent_option]

# Solve button
if st.button("🛠 Solve Problem"):
    if not problem.strip():
        st.warning("Please enter a problem to solve.")
    else:
        with st.spinner("Thinking..."):
            result = solve_problem(problem, selected_agents)
            st.success("Solution generated!")
            st.markdown("### 💡 Solution")
            st.code(result, language='markdown')
