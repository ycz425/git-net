import networkx as nx
import numpy as np
from numpy.linalg import norm


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
    user_similarities = np.zeros(len(users))
    for i in range(len(users)):
        user_similarities[i] = np.dot(user_repo_matrix[i], target_user_vector) / (norm(user_repo_matrix[i]) * target_user_vector_norm)

    top_user_indices = np.argsort(user_similarities)
    top_user_indices = top_user_indices[top_user_indices != target_user_index]

    user_to_user_scores = np.zeros(len(repos))
    for user_index in top_user_indices:
        for i in range(len(repos)):
            if user_repo_matrix[user_index, i] == 1 and user_repo_matrix[target_user_index, i] != 1:
                user_to_user_scores[i] = user_similarities[user_index]

    repo_to_repo_scores = np.zeros(len(repos))
    for i in range(len(repos)):
        if user_repo_matrix[target_user_index, i] == 1:
            for neighbor in G.neighbors(repos[i]):
                if G.nodes[neighbor]['type'] == 'repo':
                    neighbor_index = repos.index(neighbor)
                    if user_repo_matrix[target_user_index, neighbor_index] != 1:
                        repo_to_repo_scores[neighbor_index] = 1
    
    scores = 0.7 * user_to_user_scores + 0.3 * repo_to_repo_scores
    top_score_indices = np.argsort(scores)[::-1][:num]
    
    return [repos[index] for index in top_score_indices]
    