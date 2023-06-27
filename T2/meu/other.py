import numpy as np

def print_tree(node, depth=0):
    if node is None:
        return

    indent = "  " * depth
    if node.label:
        print(indent + "Action: " + node.label)
    else:
        print(indent + "Features: " + str(node.feature))
        print_tree(node.left, depth + 1)
        print_tree(node.right, depth + 1)

class Node:
    def __init__(self, feature=None, value=None, left=None, right=None, label=None):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right
        self.label = label

def generate_random_tree(max_depth):
    if max_depth == 0 or np.random.rand() < 0.5:
        label = np.random.choice(["K_DOWN", "K_UP"])
        return Node(label=label)

    feature = np.random.randint(7)  # Assuming 7 features in total
    value = np.random.uniform(-1, 1)  # Assuming feature values range from -1 to 1

    left = generate_random_tree(max_depth - 1)
    right = generate_random_tree(max_depth - 1)

    return Node(feature=feature, value=value, left=left, right=right)

def get_random_features(num_features, num_random_features):
    return np.random.choice(num_features, num_random_features, replace=False)

def improve_tree(tree, num_random_features):
    if tree.left and tree.right:
        left = improve_tree(tree.left, num_random_features)
        right = improve_tree(tree.right, num_random_features)
        return Node(left=left, right=right)
    else:
        new_features = get_random_features(7, num_random_features)  # Assuming 7 features in total
        new_layer = generate_random_tree(max_depth=1)
        return Node(feature=new_features, left=tree, right=new_layer)

def tree_depth(tree):
    if tree is None:
        return 0
    left_depth = tree_depth(tree.left)
    right_depth = tree_depth(tree.right)
    return max(left_depth, right_depth) + 1

# Example usage
max_depth = 5
num_random_features = 2

# Generate a random decision tree
random_tree = generate_random_tree(max_depth)

print("Random Tree:")
print_tree(random_tree)


# Improve the tree by adding one layer with random features
improved_tree = improve_tree(random_tree, num_random_features)

# Traverse the tree and print its structure


print("\nImproved Tree:")
print_tree(improved_tree)
