# To use: streamlit run article_writer.py 

from crewai import Agent, Crew, Task, Process
from langchain_community.tools import DuckDuckGoSearchRun
import streamlit as st

search_tool = DuckDuckGoSearchRun()

st.title('AI Research & Write')
topic = st.text_input('Topic')

if st.button('Research and Write it!.'):
    researcher = Agent(
        role='Senior Researcher',
        goal=f"Uncover groundbreaking technologies around {topic}",
        backstory="Drive by curiosity, you're at the forefront of innovation",
        verbose=True
    )

    writer = Agent(
        role="Writer",
        goal=f"Narrate compelling tech stories about {topic}",
        backstory="With a flair for simplifying complex topics, you craft engaging narratives.",
        verbose=True
    )

    research_task = Task(
        description="""
        Identify the next big trend in {topic}.
        Focus on identifying pros and cons and the overall narrative.

        Your final report should clearly articulate the key points.
        Its market opportunities, and potential risks.
        """,
        expected_output="A 3 paragraphs long report on the latest AI trends.",
        max_iter=1,
        tools=[search_tool],
        agent=researcher
    )

    write_task = Task(
        description="""
    Compose an insightful article on {topic}.
    Focus on the latest trends and how it's impacting the industry.
    This article should be easy to understand, engaging and positive.
    """,
    expected_output=f"A 4 paragraph article on {topic} advancements",
    tools=[search_tool],
    agent=writer
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential
    )

    result = crew.kickoff()
    st.write(result)