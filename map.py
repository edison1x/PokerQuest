import random
import pygame as pyg
from CONSTANTS import (
    DISPLAY_DIMENSIONS_X,
    DISPLAY_DIMENSIONS_Y,
    text_font,
    GOLD,
    RED,
    BLUE)




class GraphNode:
    """
    Represents a node within the graph, used to define rooms and connections on the map.

    Attributes:
        __id (int): The unique identifier of each node
        _x (int): The x coordinate of the node's position.
        _y (int): The y coordinate of the node's position.
        _room_type (str): The type of room (e.g., "D" for dealer, "B" for boss).
        _level (int): The level of the node in the map.
        edges (list): List of connected nodes.
    """
    def __init__(self, x ,y, level):
        """
        Initialises a GraphNode object with coordinates, level, and default values for ID and room type.

        Parameters:
        x (int): The x-coordinate of the node's position.
        y (int): The y-coordinate of the node's position.
        level (int): The level of the node in the map.
        """
        self.__id = None
        self._x = x
        self._y = y
        self._room_type = None
        self._level = level
        self.edges = []
        self.visited = False

    def visit(self, rooms, current_level, dealer_type):
        self.visited = True
        player_wins = rooms.dealer_room.start_new_round(current_level, dealer_type)
        return player_wins
    def add_edge(self, connected_node):
        """
        Adds an edge to another node.

        Parameters:
            connected_node (GraphNode): The node to connect to.
        """
        self.edges.append(connected_node)

    @property
    def x(self):
        """
        Gets the x coordinate of the node.

        Returns:
            int: the x-coordinate of the node."""
        return self._x

    @property
    def y(self):
        """
        Gets the x coordinate of the node.

        Returns:
            int: the x-coordinate of the node."""
        return self._y
    @property
    def room_type(self):
        """Returns the type of room associated with the node."""
        return self._room_type

    @room_type.setter
    def room_type(self, type):
        """
        Sets the room type for the node.

        Parameters:
            type (str): The type of room to set.
        """
        self._room_type = type

    @property
    def id(self):
        """Returns the node's ID."""
        return self.__id

    @id.setter
    def id(self, id):
        """
        Sets the node's unique ID.

        Parameters:
            id (int): The unique identifier to set for the node.
        """
        self.__id = id
    @property
    def level(self):
        """
        Gets the level of the node

        Returns:
            int: the level of the node based on its ID."""
        return self._level

    @property
    def position(self):
        """
        Gets the position of the node
        Returns:
           int,int: the x, y position of the node on the screen."""
        return self._x, self._y

    @position.setter
    def position(self, pos):
        """
        Sets the position of the node.

        Parameters:
            pos (tuple): A tuple containing new x and y coordinates.
        """
        x, y = pos
        self._x = x
        self._y = y

class Graph:
    """
    Represents a graph structure containing nodes and edges for map generation.

    Attributes:
        __nodes (dict): A dictionary of nodes in the graph, indexed by node ID.
        edges (list): A list of edges between nodes.
        __next_id (int): The ID to be assigned to the next node.
    """
    def __init__(self):
        """Initialises a new Graph instance with empty nodes and edges."""
        self.__nodes = {}
        self.edges = []
        self.__next_id = 0

    @property
    def next_id(self):
        """Returns the next ID to be assigned to a new node."""
        return self.__next_id

    @property
    def nodes(self):
        """Returns the dictionary of nodes in the graph."""
        return self.__nodes

    @property
    def nodes_keys(self):
        """Returns the keys (IDs) of the nodes in the graph."""
        return self.__nodes.keys()

    @property
    def nodes_values(self):
        """Returns the values (GraphNode instances) of the nodes in the graph."""
        return self.__nodes.values()

    def add_node(self, node):
        """
        Adds a node to the graph and assigns it a unique ID.

        Parameters:
            node (GraphNode): The node to add to the graph.
        """
        node.id = self.__next_id
        self.__nodes[node.id] = node
        self.__next_id += 1

    def remove_node(self, node_id):
        """
        Removes a node from the graph by its ID.

        Parameters:
            node_id (int): The ID of the node to remove.
        """
        if node_id in self.__nodes:
            self.__nodes.pop(node_id)

    def add_edge(self, from_node, to_node):
        """
        Adds an edge between two nodes, establishing a connection.

        Parameters:
            from_node (GraphNode): The starting node of the edge.
            to_node (GraphNode): The ending node of the edge.

        Raises:
            Exception: If one or both nodes are not in the graph.
        """
        if from_node in self.__nodes.values() and to_node in self.__nodes.values():
            from_node.add_edge(to_node)
            to_node.add_edge(from_node)
            self.edges.append((from_node, to_node))
        else:
            raise Exception(f"One or both nodes not in graph: {from_node.id}, {to_node.id}")

class MapGenerator:
    """
    Generates a map represented as a graph of interconnected rooms.

    Attributes:
        _graph (Graph): The graph structure representing the map.
        paths (list): List of paths generated within the map.
        _rows (int): The number of rows in the map.
        _cols (int): The number of columns in the map.
        __num_of_paths (int): The number of paths to be generated.
        _first_level_chosen_nodes (set): Set of nodes chosen from the first level.
        _nodes_after_first_boss (set): Set of nodes chosen after the first boss.
        __starting_node (GraphNode): The starting node of the map.
        __boss_node (GraphNode): The boss node in the map.
        __end_node (GraphNode): The end node in the map.
        __least_x (int): The least x coordinate of all nodes.
        __greatest_x (int): The greatest x coordinate of all nodes.
    """
    def __init__(self):
        """Initialises the MapGenerator and starts generating the map."""
        self._graph = Graph()
        self.paths = []
        self._rows = 10
        self._cols = 10
        self.__num_of_paths = 5
        self._nodes_not_to_connect_to = set()
        self.__starting_node = None
        self.__boss_node = None
        self.__end_node = None
        self.__least_x = DISPLAY_DIMENSIONS_X
        self.__greatest_x = 0
        self.generate_graph()

    @property
    def graph(self):
        """Returns the graph representing the map."""
        return self._graph

    @property
    def starting_node(self):
        """Returns the starting node of the map."""
        return self.__starting_node

    @starting_node.setter
    def starting_node(self, node):
        """
        Sets the starting node for the map.

        Parameters:
            node (GraphNode): The starting node to set.
        """
        self.__starting_node = node

    @property
    def end_node(self):
        """Returns the end node of the map."""
        return self.__end_node

    @end_node.setter
    def end_node(self, node):
        """
        Sets the end node for the map.

        Parameters:
            node (GraphNode): The end node to set.
        """
        self.__end_node = node

    @property
    def boss_node(self):
        """Returns the boss node of the map."""
        return self.__boss_node

    @boss_node.setter
    def boss_node(self, node):
        """
        Sets the boss node for the map.

        Parameters:
            node (GraphNode): The boss node to set.
        """
        self.__boss_node = node

    def check_boss_room_completed(self, current_node):
        """
        Checks if the boss room on level 11 is completed.

        Parameters:
            current_node (GraphNode): The current node to check.

        Returns:
            bool: True if the boss room is completed, False if not.
        """
        return current_node.level == 11 and current_node.room_type == "B"

    def generate_nodes(self):
        """Generates nodes for the map, including the starting, boss, and end nodes."""
        #Node ID 0 will be the starting node
        start_x = round(DISPLAY_DIMENSIONS_X// 2)
        start_y = round(DISPLAY_DIMENSIONS_Y// 13)
        new_starting_node = GraphNode(start_x, start_y, 0)
        self._graph.add_node(new_starting_node)
        self.starting_node = new_starting_node

        #Generate 100 nodes (levels 1-10)
        for index in range(self._rows * self._cols):
            level = (index // 10) + 1
            row = index // 10
            col = index % 10
            #Offsets take the nodes look less fixed in place
            x_offset = random.uniform(-DISPLAY_DIMENSIONS_X * 0.01, DISPLAY_DIMENSIONS_X * 0.01)
            y_offset = random.uniform(-DISPLAY_DIMENSIONS_Y * 0.01, DISPLAY_DIMENSIONS_Y * 0.01)
            #Calculate base position
            x = ((col * (1 / 10 * DISPLAY_DIMENSIONS_X)) + (DISPLAY_DIMENSIONS_X / 20)) + x_offset
            #Calculate y position based on row, ensuring it stays within the first half of the screen
            y = ((row * (1 / 13 * DISPLAY_DIMENSIONS_Y)) + (DISPLAY_DIMENSIONS_Y / 13)) + y_offset
            x = round(x)
            y = round(y)
            self._graph.add_node(GraphNode(x, y, level))

            if x < self.__least_x:
                self.__least_x = x
            if x > self.__greatest_x:
                self.__greatest_x = x

        #Add only one boss node on level 11 so all nodes on level 10 must connect to this
        boss_x = round((self.__greatest_x + self.__least_x) / 2)
        boss_y = round((11/13) * DISPLAY_DIMENSIONS_Y)
        boss_node = GraphNode(boss_x, boss_y, 11)
        self._graph.add_node(boss_node)
        self.boss_node = boss_node

        #Generate second set of 100 nodes (levels 12-21)
        for index in range(self._rows*self._cols):
            level = (index // 10) + 12
            row = index // 10
            col = index % 10
            x_offset = random.uniform(-DISPLAY_DIMENSIONS_X * 0.01, DISPLAY_DIMENSIONS_X * 0.01)
            y_offset = random.uniform(-DISPLAY_DIMENSIONS_Y * 0.01, DISPLAY_DIMENSIONS_Y * 0.01)
            x = ((col * (1 / 10 * DISPLAY_DIMENSIONS_X)) + (DISPLAY_DIMENSIONS_X / 20)) + x_offset
            base_y = (11/13) * DISPLAY_DIMENSIONS_Y # Start after the boss node
            relative_row = row + 1  # Add 1 to account for the boss node
            y = base_y + (relative_row * (1 / 13 * DISPLAY_DIMENSIONS_Y)) + y_offset
            x = round(x)
            y = round(y)

            self._graph.add_node(GraphNode(x, y, level))

        final_boss_x = start_x
        final_boss_y = round((23/13) * DISPLAY_DIMENSIONS_Y)
        final_boss_node = GraphNode(final_boss_x, final_boss_y, 22)
        self._graph.add_node(final_boss_node)
        self.end_node = final_boss_node

    def find_next_node(self, current_node):
         """
        Finds the next node to connect to based on the current node's level and type.

        Parameters:
            current_node (GraphNode): The current node from which to find the next node.

        Returns:
            GraphNode: The next node to connect to based on rules.
        """
         nodes = self._graph.nodes
         if current_node == self.__starting_node:
            next_node = self.get_any_node_above(self.__starting_node, nodes)
         elif current_node == self.__boss_node:
             next_node = self.get_any_node_above(self.__boss_node, nodes)
         elif current_node.level == 10:
             #All nodes have to connect to the guarenteed boss room
             next_node = self.__boss_node
         elif current_node.level == 21: #Last row so needs to connect to end node
            next_node = self.get_end_node(nodes)
         else:
            next_node = self.get_node_on_above_level(current_node, nodes)


         return next_node

    def get_any_node_above(self, from_node, nodes):
        """
        Connects the starting node to a unique node on level 1.

        Parameters:
            nodes (dict): A dictionary of all nodes in the graph.

        Returns:
            GraphNode: A unique node from level 1 that is connected after the starting node.
        """
        #Choose any node after on the floor above. This is for after the starting node or boss node.
        #Allows unique paths
        next_node_id = random.randint(from_node.id + 1, from_node.id + 10)
        while nodes[next_node_id] in self._nodes_not_to_connect_to: #If the chosen node has already been chosen, reselect
            next_node_id = random.randint(from_node.id + 1, from_node.id + 10)
        self._nodes_not_to_connect_to.add(nodes[next_node_id])
        return nodes[next_node_id]

    def get_end_node(self, nodes):
        """
        Connects level 21 nodes to the final boss on level 22.

        Parameters:
            nodes (dict): A dictionary of all nodes in the graph.

        Returns:
            GraphNode: The end node (boss node) at level 22.
        """
        next_node_id = self.__end_node.id
        return nodes[next_node_id]

    def get_node_on_above_level(self, current_node, nodes):
        """
        Selects one of the closest three nodes on the level above the current node.

        Parameters:
            current_node (GraphNode): The current node from which to find a node above.
            nodes (dict): A dictionary of all nodes in the graph.

        Returns:
            GraphNode: A randomly chosen node from the level above the current node.
        """
        #Normal case for nodes 1–100
        if current_node.id <= 100:
            #Determine the current level based on ID (ID ranges 1-10 for level 1, 11-20 for level 2, etc.)
            level_start = (current_node.level - 1) * 10 + 1
            level_end = current_node.level * 10
        else:
            #Since ID 101 is a level itself, we adjust levels for nodes 102 and beyond
            adjusted_node_id = current_node.id - 1  #Shift IDs by 1 after 101
            level_number = (adjusted_node_id - 1) // 10 + 1
            level_start = (level_number - 1) * 10 + 2  #Shifted by 1 to start from ID 102
            level_end = level_start + 9
        if current_node.id == level_end:
            #Node is on far left so only can connect to the one directly above or to the right of it
            next_node_id = random.randint(current_node.id + 9, current_node.id + 10)
        elif current_node.id == level_start:
            #Node is on far right so only can connect to the one directly above or to the left of it
            next_node_id = random.randint(current_node.id + 10, current_node.id + 11)
        else:
            #Node can connect to any of the three closest.
            next_node_id = random.randint(current_node.id + 9, current_node.id + 11)
        return nodes[next_node_id]

    def generate_paths(self):
        """
        Generates multiple paths in the graph based on the defined number of paths.
        """
        for _ in range(self.__num_of_paths):
            self.generate_path()

    def generate_path(self):
        """
        Generates a single path from the starting node to the end node.

        This method iteratively finds the next node until it reaches the end node,
        connecting each node along the path.
        """
        path = []
        path.append(self.__starting_node)
        current_node = path[-1]
        #Create a path from starting node to the end node adding edges in between the nodes.
        while current_node != self.__end_node:
            next_node = self.find_next_node(current_node)
            if next_node == self.__end_node:
                self._graph.add_edge(current_node, next_node)
                break

            self._graph.add_edge(current_node, next_node)
            current_node = next_node
            path.append(current_node)

        self.paths.append(path)

    def remove_unconnected_nodes(self):
        """
        Removes nodes from the graph that have no connections (edges).

        This method iterates through all nodes in the graph and finds
        any nodes that are not connected to any other nodes, removing them from the graph.
        """
        for node_id, node in list(self._graph.nodes.items()):
            if len(node.edges) == 0:  #If the node has no edges, remove it
                self._graph.remove_node(node_id)


    def assign_room_types(self):
        """
        Assigns types to rooms in the graph based on specific rules.

        This method assigns predetermined room types to specific nodes
        and then assigns other room types based on the remaining pool of room types.
        """

        bucket = self.create_room_type_bucket()
        #Assign predetermined rooms
        for node in self._graph.nodes_values:
            #0th and first floor is a guarenteed dealer room
            if node.level == 0 or node.level == 1:
                node.room_type = "D"
                bucket.remove("D")
            #Guaranteed boss levels
            elif node.level == 11 or node.level == 22:
                node.room_type = "B"
        #Iterate through remaining rooms that do not have a room type
        for node in self._graph.nodes_values:
            if node.room_type is None:
                room_type = self.get_valid_room_type(node, bucket)
                node.room_type = room_type
                print(f"{node.id} has no room type, assinging {node.room_type}")
                #Found a valid room type so remove it from the bucket
                if room_type in bucket:
                    bucket.remove(room_type)

    def get_valid_room_type(self, node, bucket):
        """
        Gets a valid room type for a given node from the room type bucket.

        Parameters:
            node (GraphNode): The node for which to find a valid room type.
            bucket (list): A list of available room types.

        Returns:
            str: A valid room type for the node, defaults to "D" if none found.
        """
        reward_room_below= self.check_previous_floor_types(node)
        for room_type in bucket:
            if reward_room_below:
                #There was a reward room below, so must be a dealer next
                return "D"
            if reward_room_below and room_type == "R":
                #Do not want to put 2 reward rooms in a row so continue
                continue
            return room_type

        #If no valid room type is found, default to "D" (dealer room)
        return "D"

    def check_previous_floor_types(self, node):
        """
        Checks if there are any reward rooms below the current node.

        Parameters:
            node (GraphNode): The current node to check for reward rooms.

        Returns:
            bool: True if a reward room is found below, False otherwise.
        """
        #Checking if a reward room is below so that the map does not put 2 rewards in a row
        is_reward_room = False
        for neighbour in node.edges:
            if neighbour.level < node.level:
                if neighbour.room_type == "R":
                    is_reward_room = True

        return is_reward_room

    def create_room_type_bucket(self):
        """
        Creates a list of available room types for assignment to nodes.

        Returns:
            list: A list of room types available for use.
        """
        #Exclude the last node as it is a boss
        num_nodes = len(self._graph.nodes_values) - 1
        room_types = [
        {"name": "R", "proportion": 0.1},
        {"name": "?", "proportion": 0.45},
        {"name": "D", "proportion": 0.45}
        ]

        total_rooms = 0
        for room in room_types:
            raw_count = room["proportion"] * num_nodes
            room["rounded_count"] = round(raw_count) #Adds the room count
            room["fractional_part"] = raw_count % 1 #Adds the fractional part
            total_rooms += room["rounded_count"]

        difference = num_nodes - total_rooms

        def get_fractional_part(room):
            return room["fractional_part"]

        if difference != 0:
            #Sort the list based on fractional parts. Descending when adding rooms, ascending when removing.
            room_types.sort(key=get_fractional_part, reverse=(difference > 0))
            for i in range(abs(difference)):
                if difference > 0:
                    #Add one room to the type with the highest fractional part
                    room_types[i]["rounded_count"] += 1
                else:
                    #Remove one room from the type with the lowest fractional part
                    room_types[i]["rounded_count"] -= 1
        #Create bucket of room types now and shuffle it
        bucket = []
        for room in room_types:
            bucket.extend([room["name"]] * room["rounded_count"])
        random.shuffle(bucket)
        return bucket

    def generate_graph(self):
        """Generates the graph by calling the appropriate methods"""
        self.generate_nodes()
        self.generate_paths()
        self.remove_unconnected_nodes()
        self.assign_room_types()

class MapVisualiser:
    """
    A class to visualise a graph-based map using Pygame.

    Attributes:
        _map_generator (MapGenerator): The map generator that produces the graph.
        _graph (Graph): The graph representing the map structure.
        __display_dimensions (tuple): The dimensions of the display window.
        __display (pyg.Surface): The Pygame surface for drawing.
        current_level (int): The current level being visualised.
        completed_nodes (list): A list of nodes that have been completed.
        __font (pyg.font.Font): The font used for rendering text.
        __circle_size (int): The size of the circles representing nodes.

    Parameters:
        map_generator (MapGenerator): An instance of the map generator.
        display_dimensions (tuple): The width and height of the display.
        display (pyg.Surface): The Pygame surface on which to visualize the map.
    """
    def __init__(self, map_generator, display):
        self._map_generator = map_generator
        self._graph = self._map_generator.graph
        self.__display = display
        self.current_level = 0
        self.completed_nodes = []
        self.__font = text_font(20)
        self.__circle_size = 20
        self.scroll_level = 0

    def visualise_graph(self, current_node):
        """
        Main loop to visualize the graph on the Pygame window.

        This method draws the nodes and edges of the graph within the current
        level view. Different colours represent the current node (red), completed nodes (green), and potential
        next nodes (gold-ish).

        Parameters:
            current_node (GraphNode): The current node being visualized.
        """
        self.__display.fill((0, 0, 0))

        #Draw edges between nodes
        for edge in self._graph.edges:
            node1, node2 = edge
            #Check if both nodes are within the current level view

            #Scale positions for drawing
            scaled_pos1 = self.scale_position(node1)
            scaled_pos2 = self.scale_position(node2)
            if self.scroll_level != 0:
                scaled_pos1 = self.update_positions_after_scroll(node1)
                scaled_pos2 = self.update_positions_after_scroll(node2)
            #Draw a red line between nodes
            pyg.draw.line(self.__display, (255, 0, 0), scaled_pos1, scaled_pos2, 2)

        #Draw nodes within the current level view
        for node in self._graph.nodes_values:
            #Scale position for current node
            scaled_pos = self.scale_position(node)
            if self.scroll_level != 0:
                scaled_pos = self.update_positions_after_scroll(node)
            colour = self.get_node_colour(node, current_node)
            pyg.draw.circle(self.__display, colour, scaled_pos, 20)
            label = self.__font.render(node.room_type, True, (255, 255, 255))
            self.__display.blit(label, (scaled_pos[0] - 10, scaled_pos[1] - 10))

    def get_node_colour(self, node, current_node):
        """Determine the color based on node status."""
        if node.id == current_node.id:
            return RED  #Red for current node
        elif self.completed_nodes and node in self.completed_nodes[-1].edges:
            if node.level > self.completed_nodes[-1].level:
                return GOLD #Gold for potential next nodes

        return BLUE  #Default blue for undiscovered nodes

    def scale_position(self, node):
        """Scale node position to fit current view window"""
        x = node.x
        #Scale y position to fit within visible window
        y = ((node.level - self.current_level) / 10) * DISPLAY_DIMENSIONS_Y + self.__circle_size + 1
        return (round(x), round(y))

    def update_positions_after_scroll(self, node):
        """Displays nodes that are now in view"""
        x = node.x
        y = ((node.level - self.scroll_level) / 10) * DISPLAY_DIMENSIONS_Y + self.__circle_size + 1
        return (round(x), round(y))


    def handle_click(self, mouse_pos):
        """
        Handles mouse click events and returns the room (node) clicked on.

        Parameters:
            mouse_pos: The position of the mouse click.

        Returns:
            node: The clicked room node if one was clicked, else None.
        """
        #Check each node to see if it was clicked
        for node in self._graph.nodes_values:
            if self.current_level <= node.level <= self.current_level + 10:
                scaled_pos = self.scale_position(node)
                #Check if the click is within the node's radius
                if pyg.Vector2(mouse_pos).distance_to(scaled_pos) < 20:
                    return node

        return None #Return None if no node was clicked