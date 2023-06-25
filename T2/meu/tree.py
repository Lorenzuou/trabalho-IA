import random
import numpy as np

# Constants for PSO
POPULATION_SIZE = 50
MAX_ITERATIONS = 100
C1 = 2.0  # cognitive parameter
C2 = 2.0  # social parameter
W = 0.7  # inertia weight

# Constants for the Dino game
THRESHOLD = 0.5  # Decision threshold for action selection

class Node:
    def __init__(self, feature=None, threshold=None, action=None, left=None, right=None):
        self.feature = feature
        self.threshold = threshold
        self.action = action
        self.left = left
        self.right = right

class KeyClassifier:
    def __init__(self, state):
        self.state = state
        self.decision_tree = None
        print(self.state)


    def keySelector(self, distance, obHeight, game_speed, obType, nextObDistance, nextObHeight,
                                             nextObType):
        features = [distance, obHeight, game_speed, obType, nextObDistance, nextObHeight,
                                             nextObType]
        # return self.predict_action(self.decision_tree, features)
        return "K_UP"

    def updateState(self, state):
        self.state = state

    def train(self, data, labels):
        num_features = len(data[0])
        population = []
        global_best = float('-inf')
        global_best_position = None

        for _ in range(POPULATION_SIZE):
            feature_indices = random.sample(range(num_features), random.randint(1, num_features))
            tree = self.generate_random_tree(feature_indices)
            population.append(tree)

        for _ in range(MAX_ITERATIONS):
            for i in range(POPULATION_SIZE):
                particle = population[i]
                fitness = self.evaluate_fitness(particle, data, labels)

                if fitness > global_best:
                    global_best = fitness
                    global_best_position = particle

                for node in self.get_nodes(particle):
                    if random.random() < 0.5:
                        node.feature = random.choice(range(num_features))

                for node in self.get_leaf_nodes(particle):
                    node.action = random.choice(['K_DOWN', 'K_UP'])
                    node.threshold = random.uniform(0.0, 1.0)

            for particle in population:
                for node in self.get_nodes(particle):
                    if random.random() < W:
                        global_node = self.get_node_by_id(global_best_position, node.id)
                        node.feature = global_node.feature

        self.decision_tree = global_best_position

    def generate_random_tree(self, feature_indices):
        if random.random() < 0.5:
            action = random.choice(['K_DOWN', 'K_UP'])
            return Node(action=action)
        
        # generate a random feature
        feature = random.choice(feature_indices)
        threshold = random.uniform(0.0, 1.0)

        left_subtree = self.generate_random_tree(feature_indices)
        right_subtree = self.generate_random_tree(feature_indices)

        return Node(feature=feature, threshold=threshold, left=left_subtree, right=right_subtree)

    def evaluate_fitness(self, tree, data, labels):
        correct_predictions = 0
        for i in range(len(data)):
            if self.predict_action(tree, data[i]) == labels[i]:
                correct_predictions += 1
        return correct_predictions / len(data)

    def predict_action(self, tree, features):
        node = tree
        while node.feature is not None:
            if features[node.feature] < node.threshold:
                node = node.left
            else:
                node = node.right
        return node.action

    def get_nodes(self, tree):
        nodes = []
        stack = [tree]
        while stack:
            node = stack.pop()
            nodes.append(node)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return nodes

    def get_leaf_nodes(self, tree):
        return [node for node in self.get_nodes(tree) if node.feature is None]

    def get_node_by_id(self, tree, node_id):
        stack = [tree]
        while stack:
            node = stack.pop()
            if node.id == node_id:
                return node
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return None

    # PSO algorithm
    def pso_decision_tree(self,data, labels):
        num_features = len(data[0])
        population = []
        global_best = float('-inf')
        global_best_position = None

        # Initialize particles
        for _ in range(POPULATION_SIZE):
            feature_indices = random.sample(range(num_features), random.randint(1, num_features))
            tree = self.generate_random_tree(feature_indices)
            population.append(tree)

        for _ in range(MAX_ITERATIONS):
            for i in range(POPULATION_SIZE):
                particle = population[i]
                fitness = self.evaluate_fitness(particle, data, labels)

                if fitness > global_best:
                    global_best = fitness
                    global_best_position = particle

                # Update particle's position and velocity
                for node in self.get_nodes(particle):
                    if random.random() < 0.5:
                        node.feature = random.choice(range(num_features))

                # Update particle's action and threshold
                for node in self.get_leaf_nodes(particle):
                    node.action = random.choice(['K_DOWN', 'K_UP'])
                    node.threshold = random.uniform(0.0, 1.0)

            # Update particle's position based on global best
            for particle in population:
                for node in self.get_nodes(particle):
                    if random.random() < W:
                        global_node = self.get_node_by_id(global_best_position, node.id)
                        node.feature = global_node.feature

        return global_best_position

# Example usage
if __name__ == '__main__':
    # Instantiate the KeyClassifier
    key_classifier = KeyClassifier(state)

    # Prepare the training data and labels
    training_data = [...]  # Your training data here
    labels = [...]  # Your corresponding labels here

    # Train the decision tree model
    key_classifier.train(training_data, labels)

    # Use the trained model for prediction
    distance = ...  # The distance value for prediction
    obHeight = ...  # The obHeight value for prediction
    speed = ...  # The speed value for prediction
    obType = ...  # The obType value for prediction

    action = key_classifier.keySelector(distance, obHeight, speed, obType)
    print("Predicted action:", action)
