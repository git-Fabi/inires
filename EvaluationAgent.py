import logging

class EvaluationAgent:
    def __init__(self):
        self.criteria = []
        logging.basicConfig(level=logging.INFO)

    def evaluate_solution(self, solution):
        feedback = f'Evaluating: {solution}'
        self.criteria.append(feedback)
        logging.info(feedback)
        return feedback
