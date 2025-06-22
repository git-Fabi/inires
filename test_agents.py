import logging
from SolutionGeneratorAgent import SolutionGeneratorAgent
from EvaluationAgent import EvaluationAgent

# Initialize agents
solution_generator = SolutionGeneratorAgent()
evaluation_agent = EvaluationAgent()

# Test solution generation
problem = 'example problem'
solution = solution_generator.generate_solution(problem)
print(solution)

# Test evaluation of the generated solution
feedback = evaluation_agent.evaluate_solution(solution)
print(feedback)
