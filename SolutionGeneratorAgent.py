import logging

class SolutionGeneratorAgent:
    def __init__(self):
        self.solutions = []
        logging.basicConfig(level=logging.INFO)

    def generate_solution(self, problem):
        solution = f'Solution for {problem}'
        self.solutions.append(solution)
        logging.info(f'Generated solution: {solution}')
        return solution
