import networkx as nx
import numpy as np
from numpy.linalg import norm
import random


def recommend_repos(G: nx.Graph, target_user: int, num: int) -> list[int]:
    users = [node for node in G.nodes() if G.nodes[node]['type'] == 'user']
    repos = [node for node in G.nodes() if G.nodes[node]['type'] == 'repo']
    user_repo_matrix = np.zeros((len(users), len(repos)))

    for i in range(len(users)):
        for j in range(len(repos)):
            if G.has_edge(users[i], repos[j]):
                user_repo_matrix[i, j] = 1

    target_user_index = users.index(target_user)
    target_user_vector = user_repo_matrix[target_user_index]
    target_user_vector_norm = norm(target_user_vector)
    cosine_similarities = np.zeros(len(users))
    for i in range(len(users)):
        cosine_similarities[i] = np.dot(user_repo_matrix[i], target_user_vector) / (norm(user_repo_matrix[i]) * target_user_vector_norm)

    top_user_indices = np.argsort(cosine_similarities)[::-1]
    top_user_indices = top_user_indices[top_user_indices != target_user_index]

    results = set()
    for user_index in top_user_indices:
        for i in range(len(repos)):
            if user_repo_matrix[user_index, i] == 1 and user_repo_matrix[target_user_index, i] != 1:
                results.add(repos[i])
    
    return random.sample(results, num)
    