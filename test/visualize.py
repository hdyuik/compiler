from collections import defaultdict, deque
from graphviz import Digraph, Graph

from parser.ast import Leaf

def output_fsm(fsm, filename, eq_symbols=None):
    fsm_graph = Digraph(graph_attr={"rankdir": "LR"})

    for state in fsm.states:
        name = str(state.index)

        label = str(state.index) + '\n' + str(state.items)
        if hasattr(state.items, "nfa_states"):
            for nfa_state in state.items.nfa_states:
                label += ('\n' + str(nfa_state.items))

        if state is fsm.start_state:
            fsm_graph.node(name, label, shape="box")
        elif state in fsm.accepting_states:
            fsm_graph.node(name, label, _attributes={"peripheries": "2"})
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

    if eq_symbols:
        symbol_mapper = eq_symbols.reversed_mapper
        mapper_graph = Graph(node_attr={"shape": "record"}, graph_attr={"rankdir": "LR"})

        for index, symbols in symbol_mapper.items():
            text = ""
            if len(symbols) > 10:
                for symbol in symbols:
                    if str(symbol).isprintable() and len(text) < 10:
                        text += str(symbol)
            else:
                text = ','.join([str(symbol) for symbol in symbols])

            text = text.replace("|", "\|")
            text = text.replace(">", "\>")
            text = text.replace("<", "\<")
            text = text.replace("{", "\{")
            text = text.replace("}", "\}")
            text = text.replace("\\", "\\\\")


            mapper_graph.node(str(index), "{" +"{0}|{1}".format(text, str(index)) + "}")

        mapper_graph.render(filename+"_mapper", cleanup=True)


def output_ast(ast, filename):
    graph = Digraph()

    index = 1
    graph.node(str(index), label=str(ast.root_symbol) + '\n' + str(ast.rule))
    pending = deque()
    pending.append((ast, index))
    while pending:
        cur_ast, name = pending.pop()
        for child in cur_ast.children:
            index += 1
            if isinstance(child, Leaf):
                graph.node(str(index), label=str(child.actual_input))
            else:
                graph.node(str(index), label=str(child.root_symbol) + '\n' + str(child.rule))
            graph.edge(str(name), str(index))
            pending.append((child, index))

    graph.render(filename, cleanup=True)

