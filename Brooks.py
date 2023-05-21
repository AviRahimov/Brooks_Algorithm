import tkinter as tk

class GraphColoringApp(tk.Tk):
    """
    Graph Coloring Application using Brooks' Coloring Algorithm.

    This application allows users to draw vertices on a canvas, connect them with edges, and color the graph
    using the Brooks' Coloring Algorithm. The vertices are represented as circles, and their colors are displayed
    as numbers inside the circles.

    Attributes:
        canvas (tk.Canvas): The canvas widget for drawing the graph.
        clear_button (tk.Button): Button widget to clear the graph.
        color_button (tk.Button): Button widget to color the graph.
        connect_button (tk.Button): Button widget to connect vertices.
        vertices (list): List of Vertex objects representing the graph vertices.
        edges (list): List of tuples representing the edges between connected vertices.
        selected_vertex (Vertex or None): The currently selected vertex during edge connection.
        connect_mode (bool): Flag to indicate whether the connect mode is active or not.
    """

    def __init__(self):
        """
        Initialize the GraphColoringApp class.
        """
        tk.Tk.__init__(self)
        self.title("Brooks' Coloring Algorithm")
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.add_vertex)
        self.clear_button = tk.Button(self, text="Clear Graph", command=self.clear_graph)
        self.clear_button.pack(side=tk.LEFT)
        self.color_button = tk.Button(self, text="Color Graph", command=self.color_graph)
        self.color_button.pack(side=tk.LEFT)
        self.connect_button = tk.Button(self, text="Connect Vertices", command=self.connect_vertices)
        self.connect_button.pack(side=tk.LEFT)
        self.vertices = []
        self.edges = []
        self.selected_vertex = None
        self.connect_mode = False

    def clear_graph(self):
        """
        Clear the graph by deleting all vertices and edges on the canvas.
        """
        self.canvas.delete("all")
        self.vertices = []
        self.edges = []
        self.selected_vertex = None
        self.connect_mode = False
        self.canvas.bind("<Button-1>", self.add_vertex)

    def color_graph(self):
        """
        Color the graph using Brooks' Coloring Algorithm.

        This method applies the Brooks' Coloring Algorithm to color the graph vertices
        in a way that no two adjacent vertices have the same color. The colors are displayed
        inside the circles representing the vertices on the canvas.
        """
        if len(self.vertices) == 0:
            return
        # Clear previous colors
        for vertex in self.vertices:
            vertex.color = None

        # Sort vertices in descending order of degrees
        sorted_vertices = sorted(self.vertices, key=lambda v: len(v.connected_vertices), reverse=True)
        colors = [False] * len(sorted_vertices)
        colors[0] = True  # Color the first vertex with 0
        for vertex in sorted_vertices:
            available_colors = [True] * len(sorted_vertices)  # All colors are initially available
            for neighbor in vertex.connected_vertices:
                if neighbor.color is not None:
                    available_colors[neighbor.color] = False  # Mark neighbor's color as unavailable
            for color in range(len(sorted_vertices)):
                if available_colors[color]:
                    vertex.color = color
                    colors[vertex.index] = color
                    break
        for vertex in self.vertices:
            x, y = vertex.position
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=self.color_to_hex(vertex.color))
            self.canvas.create_text(x, y, text=str(vertex.color), fill="white")

    def connect_vertices(self):
        """
        Activate the connect mode to connect vertices.

        This method allows the user to connect vertices by selecting them on the canvas.
        The vertices are connected by drawing lines between them.
        """
        if len(self.vertices) < 2:
            return
        self.connect_mode = True
        self.canvas.bind("<Button-1>", self.select_vertex)

    def select_vertex(self, event):
        """
        Select vertices for edge connection.

        This method is called when the connect mode is active and the user clicks on a vertex.
        It connects the selected vertex with the previously selected vertex by creating an edge
        and drawing a line between them on the canvas.

        Args:
            event (tk.Event): The mouse click event containing the coordinates of the click.

        """
        x, y = event.x, event.y
        for vertex in self.vertices:
            vx, vy = vertex.position
            if abs(x - vx) <= 10 and abs(y - vy) <= 10:
                if self.selected_vertex is None:
                    self.selected_vertex = vertex
                    return
                if self.selected_vertex != vertex:
                    self.edges.append((self.selected_vertex, vertex))
                    self.canvas.create_line(self.selected_vertex.position, vertex.position)
                    self.selected_vertex.connected_vertices.append(vertex)
                    vertex.connected_vertices.append(self.selected_vertex)
                    self.selected_vertex = None
                    return
        self.selected_vertex = None

    def add_vertex(self, event):
        """
        Add a vertex to the graph.

        This method is called when the user clicks on the canvas to add a new vertex.
        It creates a Vertex object, adds it to the list of vertices, and displays it as a circle
        on the canvas.

        Args:
            event (tk.Event): The mouse click event containing the coordinates of the click.
        """
        x, y = event.x, event.y
        vertex = Vertex((x, y), len(self.vertices))
        self.vertices.append(vertex)
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white")
        self.canvas.create_text(x, y, text=str(vertex.index))

    @staticmethod
    def color_to_hex(color):
        """
        Convert color index to hexadecimal color code.

        This static method converts the color index to a hexadecimal color code.
        It uses a predefined list of color codes and wraps around when the index exceeds
        the length of the list.

        Args:
            color (int): The color index.

        Returns:
            str: The hexadecimal color code.

        """
        hex_values = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF"]
        return hex_values[color % len(hex_values)]


class Vertex:
    """
    Class representing a graph vertex.

    Each vertex has a position on the canvas, a list of connected vertices,
    a color assignment, and an index.

    Attributes:
        position (tuple): The position (x, y) of the vertex on the canvas.
        connected_vertices (list): List of connected Vertex objects.
        color (int or None): The color assigned to the vertex.
        index (int): The index of the vertex in the graph.

    """

    def __init__(self, position, index):
        """
        Initialize the Vertex class.

        Args:
            position (tuple): The position (x, y) of the vertex on the canvas.
            index (int): The index of the vertex in the graph.

        """
        self.position = position
        self.connected_vertices = []
        self.color = None
        self.index = index

    def __repr__(self):
        """
        Return a string representation of the vertex.

        Returns:
            str: String representation of the vertex.

        """
        return f"Vertex({self.position})"


if __name__ == "__main__":
    app = GraphColoringApp()
    app.mainloop()
