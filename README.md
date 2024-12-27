# GitNet: GitHub Graph Analysis and Recommendation

This project explores the relationships between GitHub users and repositories through graph analysis. Leveraging the GitHub API, it constructs and analyzes a graph where:
- **Nodes** represent repositories and users.
- **Edges** represent relationships such as:
  - Forking relationships between repositories.
  - Starring relationships between users and repositories.

## Features

### Graph Construction
- **Repositories as Nodes**: Each GitHub repository is represented as a node.
- **Users as Nodes**: Each GitHub user is represented as a node.
- **Edges**:
  - Between repositories: Representing forking relationships.
  - Between users and repositories: Representing starring relationships.

### Data Analysis
The project includes the following graph analysis features:
- **Connected Components Analysis**: Identifying distinct clusters of nodes within the graph.
- **Degree Centrality** (not available through UI): Measuring the importance of nodes based on the number of direct connections.
- **Betweenness Centrality** (not available through UI): Identifying nodes that act as bridges between different parts of the graph.
- **Louvain Community Detection**: Visualizing communities within the graph using modularity-based clustering.

### Recommendation System
- A hybrid recommendation algorithm:
  - **Collaborative Filtering**: Suggesting repositories based on similar users.
  - **Graph-Based Recommendations**: Suggesting neighboring repositories based on graph structure.

### Visualization
- Basic visualizations using **Plotly** to:
  - Display the graph structure.
  - Highlight communities and connected components.
- Further improvements to visualizations are planned.

## Usage

### Prerequisites
- Python 3.7+
- GitHub fine-grained access token (for fetching data from API).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ycz425/git-net.git
   cd git-net
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project
1. Create a .env file and set up your GitHub fine-grained access token as an environment variable (only necessary for fetching data from GitHubAPI):
   ```Python
   GITHUB_FINE_GRAINED_ACCESS_TOKEN = <your_token_here>
   ```
2. Run the script to construct the graph and analyze the data:
   ```bash
   python main.py
   ```
3. Visualize the graph and analysis results in your browser. Click on user nodes to generate recommendations.
4. Explore other algorithms and functions in ```graph.py```.

## Future Plans
- Enhanced visualizations with more interactive features.
- Integration with advanced machine learning models for recommendations.
- Scalability improvements for handling large datasets.

## Contributing
Contributions are welcome! Please feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments
- **NetworkX** for graph analysis.
- **Plotly** for visualizations.
- **Dash** for web interface.
- **GitHub API** for providing access to repository and user data.

---

Feel free to reach out if you have any questions or feedback!
