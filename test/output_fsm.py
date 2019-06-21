from collections import defaultdict
from graphviz import Digraph

def output_fsm(fsm, filename):
    graph = Digraph()
    for state in fsm.states:
        name = str(state.index)
        label = str(state.items)

        if state is fsm.start_state:
            graph.node(name, label, shape="box")
        elif state in fsm.accepting_states:
            graph.node(name, label, shape="doublecircle")
        else:
            graph.node(name, label)


    folded_edges = defaultdict(set)
    for edge in fsm.edges:
        src = str(edge.src_state.index)
        dest = str(edge.dest_state.index)
        symbol = str(edge.symbol)
        folded_edges[(src, dest)].add(symbol)

    for conn, symbol in folded_edges.items():
        graph.edge(conn[0], conn[1], ",".join(symbol))
    graph.render(filename, cleanup=True)