from random import sample
from collections import defaultdict
from graphviz import Digraph, Graph

def output_fsm(fsm, filename, symbol_mapper=None):
    fsm_graph = Digraph()
    for state in fsm.states:
        name = str(state.index)
        label = str(state.items)

        if state is fsm.start_state:
            fsm_graph.node(name, label, shape="box")
        elif state in fsm.accepting_states:
            fsm_graph.node(name, label, shape="doublecircle")
        else:
            fsm_graph.node(name, label)


    folded_edges = defaultdict(set)
    for edge in fsm.edges:
        src = str(edge.src_state.index)
        dest = str(edge.dest_state.index)
        symbol = str(edge.symbol)
        folded_edges[(src, dest)].add(symbol)

    for conn, symbol in folded_edges.items():
        fsm_graph.edge(conn[0], conn[1], ",".join(symbol))

    fsm_graph.render(filename, cleanup=True)

    if symbol_mapper:
        mapper_graph = Graph(node_attr={"shape": "record"})

        for index, symbols in symbol_mapper.items():
            if len(symbols) > 10:
                text = ','.join(sample(symbols, 10))
            else:
                text = ','.join(symbols)

            text = text.replace("|", "\|")
            text = text.replace(">", "\>")
            text = text.replace("<", "\<")
            text = text.replace("{", "\{")
            text = text.replace("}", "\}")
            text = text.replace("\\", "\\\\")

            mapper_graph.node(str(index), "{0}|{1}".format(text, str(index)))

        mapper_graph.render(filename+"_mapper", cleanup=True)