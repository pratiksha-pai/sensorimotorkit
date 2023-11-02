from graphviz import Digraph


# Initialize a new Digraph object to correct the issues
flowchart_corrected = Digraph('CorrectedSoftwareFlowchart', node_attr={'style': 'filled', 'fillcolor': 'lightyellow'})
flowchart_corrected.attr(size='10,10')

# Add nodes
flowchart_corrected.node('A', 'Main Process')
flowchart_corrected.node('B', 'Sync Block')
flowchart_corrected.node('C', 'Start All Sub-processes')
flowchart_corrected.node('D', 'Stop Acquisition')
flowchart_corrected.node('E', 'In-memory Storage')
flowchart_corrected.node('F', 'End of Session')
flowchart_corrected.node('G', 'Post-processing')

# Sub-process nodes
flowchart_corrected.node('C1', 'Body Cam 1')
flowchart_corrected.node('C2', 'Body Cam 2')
flowchart_corrected.node('C3', 'Dart Cam')
flowchart_corrected.node('C4', 'EMG Data')
flowchart_corrected.node('C5', 'EEG Data')
flowchart_corrected.node('C6', 'Motion Gloves')
flowchart_corrected.node('C7', 'Eye Tracking')

# Post-process nodes
flowchart_corrected.node('G1', 'PKL -> Images')
flowchart_corrected.node('G2', 'Apply Tracking')

# Add edges
flowchart_corrected.edge('A', 'B')
flowchart_corrected.edge('B', 'C')
flowchart_corrected.edge('C', 'E')
flowchart_corrected.edge('D', 'E')
flowchart_corrected.edge('E', 'F')
flowchart_corrected.edge('F', 'G')
flowchart_corrected.edge('G1', 'G2')

# Edges for subprocesses
flowchart_corrected.edge('C', 'C1')
flowchart_corrected.edge('C', 'C2')
flowchart_corrected.edge('C', 'C3')
flowchart_corrected.edge('C', 'C4')
flowchart_corrected.edge('C', 'C5')
flowchart_corrected.edge('C', 'C6')
flowchart_corrected.edge('C', 'C7')

# Edges from "Stop Acquisition" to all subprocesses
flowchart_corrected.edge('D', 'C1')
flowchart_corrected.edge('D', 'C2')
flowchart_corrected.edge('D', 'C3')
flowchart_corrected.edge('D', 'C4')
flowchart_corrected.edge('D', 'C5')
flowchart_corrected.edge('D', 'C6')
flowchart_corrected.edge('D', 'C7')

# Edges for post-process
flowchart_corrected.edge('G', 'G1')
flowchart_corrected.edge('G', 'G2')

# Render the final corrected flowchart
flowchart_corrected.render('Final_Corrected_Software_Flowchart.png')
