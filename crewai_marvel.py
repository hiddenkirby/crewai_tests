from crewai import Agent, Task, Crew, Process
from marvel import fetch_marvel_characters
from langchain_openai import ChatOpenAI

# Adjusted agent definitions

donald_trump = Agent(
    role='Event Host',
    goal='Hosts the event in the Trump Tower',
    backstory='Donald Trump, a millionaire and former president, hosts a gala event.'
)

# Define the task of identifying the superhero attacker

john_mcclane = Agent(
    max_iter=2,
    role='Action Hero',
    goal='Identify and stop the superhero attacker',
    backstory="""
      John McClane, an Action Hero known for his problem-solving skills 
      in crisis situations, is on a mission to identify and stop the superhero attacker. 
      By analyzing clues on-site and interacting with the Marvel API, 
      he plans to unveil the superhero's identity.
    """,
    tools=[fetch_marvel_characters], 
)

identify_superhero = Task(
    description="Analyze the clues left by the superhero to identify them using the Marvel API. Clue: A NYPD fan sticker was found.",
    steps=[
        "Use the Marvel API to find matches for the clues.",
        "Determine the superhero's identity and motive.",
        "Devise a plan to communicate with the superhero and resolve the crisis.", 
    ]
)

# Create the crew with agents and tasks
crew = Crew(
    agents=[donald_trump, john_mcclane],
    tasks=[identify_superhero],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(temperature=0, model="gpt-4"),
)

# Kickoff the crew process 
result = crew.kickoff()