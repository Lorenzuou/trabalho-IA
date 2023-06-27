class PSODecisionTree:
    def __init__(self, num_particles, max_iterations):
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.particles = []
        self.global_best_fitness = float('-inf')
        self.global_best_solution = None

    def initialize_particles(self, num_features):
        for _ in range(self.num_particles):
            particle = {
                'position': np.random.randint(2, size=num_features),
                'velocity': np.zeros(num_features),
                'best_position': None,
                'best_fitness': float('-inf')
            }
            self.particles.append(particle)

    def evaluate_fitness(self, particle, observations):
        features = np.where(particle['position'] == 1)[0]
        
        if len(features) == 0:
            return float('-inf')
        
        # Select relevant observations based on selected features
        selected_observations = [observations[i] for i in features]
        selected_observations = np.array(selected_observations).reshape(1, -1)
        
        # Create a decision tree classifier with selected features
        clf = DecisionTreeClassifier()
        clf.fit(selected_observations)
        
        # Predict the action using the decision tree
        action = clf.predict(selected_observations)

        return action[0]

    def update_particle(self, particle, observations):
        inertia_weight = 0.5
        cognitive_weight = 1.0
        social_weight = 1.0

        for i in range(len(particle['position'])):
            r1, r2 = random.random(), random.random()
            cognitive_component = cognitive_weight * r1 * (particle['best_position'][i] - particle['position'][i])
            social_component = social_weight * r2 * (self.global_best_solution[i] - particle['position'][i])
            particle['velocity'][i] = inertia_weight * particle['velocity'][i] + cognitive_component + social_component
            particle['position'][i] = int(np.round(1 / (1 + np.exp(-particle['velocity'][i]))))

        action = self.evaluate_fitness(particle, observations)

        if action is not None:
            particle['best_position'] = particle['position'].copy()

        return action

    def update_global_best(self):
        for particle in self.particles:
            if particle['best_position'] is not None:
                self.global_best_solution = particle['best_position'].copy()
                break

    def play(self, observations, num_features):
        self.initialize_particles(num_features)
        iteration = 0

        while iteration < self.max_iterations:
            for particle in self.particles:
                action = self.update_particle(particle, observations)
                if action is not None:
                    return action
            self.update_global_best()
            iteration += 1

        return None

# Example usage
if __name__ == '__main__':
    num_features = 7
    num_particles = 10
    max_iterations = 50

    # Example observations
    observations = [100, 20, 3, 1, 50, 10, 2]

    pso_dt = PSODecisionTree(num_particles, max_iterations)
    action = pso_dt.play(observations, num_features)

    if action is not None:
        print("Action:", action)
    else:
        print("No valid action found.")