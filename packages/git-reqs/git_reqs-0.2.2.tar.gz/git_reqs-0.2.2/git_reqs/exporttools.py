import os.path
import xlwt
import networkx as nx
from networkx.drawing.nx_pydot import to_pydot

def convert_to_xls(reqmodule):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Reqs')

    for i, field in enumerate(reqmodule.fields):
        for k, req in enumerate(reqmodule.ordered_req_names):
            if field == "Req-Id":
                sheet.write(k+1, i, req)
            elif field in reqmodule.reqs.nodes[req].keys():
                sheet.write(k+1, i, reqmodule.reqs.nodes[req][field])

        sheet.write(0, i, field)
    workbook.save(reqmodule.module_path + "/test.xls")


def convert_to_markdown(reqmodule, hugo=False):
    md_file = open(reqmodule.module_path + "/reqs.md", 'w')
    if hugo:
        md_file.write('---\n'
                      'title: ' + os.path.basename(reqmodule.module_path) + '\n' 
                      'weight: 1\n'
                      'markup: mmark\n'
                       '---\n')
        
    for req in reqmodule.ordered_req_names:

        
        if 'Formatting' in reqmodule.reqs.nodes[req].keys():
            formatting = reqmodule.reqs.nodes[req]['Formatting']
        else:
            formatting = ''

        if formatting.startswith('Heading'):
            if '_' in formatting:
                heading_level = int(formatting.split('_')[1])
            else:
                heading_level = 1
            preformatting = '#'*heading_level
            description = ' ' + reqmodule.reqs.nodes[req]['Description']
            req_nr_format = '*[' + req + ']*'
            line_ending = '\n\n'
        elif 'Table' in formatting: 
            preformatting = '|'
            # Handle both |a|b|c| and a|b|c
            description = '|'.join([x for x in reqmodule.reqs.nodes[req]['Description'].split('|') if x])
            if 'Heading' in formatting:
                description += '| Req-Id |'
                description += '\n' + '|' + '|'.join(['-'*len(x) for x in description.split('|') if x])
            req_nr_format = '| *' + req + '*'
            line_ending = ' |\n'
        elif 'BulletList' in formatting: 
            if '_' in formatting:
                bullet_level = int(formatting.split('_')[1])
            else:
                bullet_level = 1
            preformatting = '  '*bullet_level + '- '
            description = reqmodule.reqs.nodes[req]['Description']
            req_nr_format = '*[' + req + ']*'
            line_ending = '\n\n'
        elif 'Italic' in formatting: 
            preformatting = ''
            description = '*' + reqmodule.reqs.nodes[req]['Description'] + '*'
            req_nr_format = '*[' + req + ']*'
            line_ending = '\n\n'
        else:
            preformatting = ''
            description = reqmodule.reqs.nodes[req]['Description']
            req_nr_format = '*[' + req + ']*'
            line_ending = '\n\n'

        md_text = preformatting + description
        if reqmodule.reqs.nodes[req]['Type'] == 'Requirement':
            md_text += ' ' + req_nr_format
        md_text += line_ending

        md_file.write(md_text) 
    md_file.close()


def create_report(project, reqmodule):
    md_file = open(project.modules[reqmodule].module_path + "/report.md", 'w')

    for req in project.modules[reqmodule].ordered_req_names:

        md_file.write(project.reqs.nodes[req]['Description'] +
                      " [" + req + "]\n\n")

        subgraph, ancestors, descendants = project.get_related_reqs(req)
        roots = [v for v, d in subgraph.in_degree() if d == 0]
        leaves = [v for v, d in subgraph.out_degree() if d == 0]

        for node in subgraph.nodes:
            for key in list(subgraph.nodes[node].keys()):
                if key not in ['Description', 'color']:
                    subgraph.nodes[node].pop(key)

        if len(subgraph) > 1:
            pos = nx.spiral_layout(subgraph)
            nx.draw(subgraph, pos=pos)

            dot = to_pydot(subgraph)
            desc_nodes = [req]
            if len(ancestors) < 3:
                desc_nodes.extend(ancestors)
            if len(descendants) < 3:
                desc_nodes.extend(descendants)

            for node_name in desc_nodes:
                print(node_name)
                node = dot.get_node(node_name)[0]
                if 'Description' in node.obj_dict['attributes'].keys():
                    Desc = node.obj_dict['attributes']['Description']
                    Desc = Desc[:100] + '...' if len(Desc) > 100 else Desc 
                    node.set_label(node_name + '\n' + Desc)
                
            dot.get_node(req)[0].set_color('blue')

            md_file.write('```{.graphviz caption="%s"}\n' % req)
            md_file.write(dot.to_string())
            md_file.write('```\n\n')

    md_file.close()

def draw_bokeh(reqmodule, req=None):
    from bokeh.io import output_file, show
    from bokeh.models import (BoxSelectTool, BoxZoomTool, ResetTool, Oval, Circle, Text,EdgesAndLinkedNodes, HoverTool,
                              MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool, )
    from bokeh.palettes import Spectral4
    from bokeh.plotting import figure, from_networkx
    from bokeh.models import ColumnDataSource, LabelSet

    if req:
        G, ancestors, descendants = reqmodule.get_related_reqs(req)
    else:
        G = reqmodule.reqs

    plot = figure(title="Requirement connection visualization", x_range=(-2, 2), y_range=(-2, 2¶),
                  tools="", toolbar_location=None)

    Fields = [("Req-Id", "@index")]
    for field in reqmodule.fields:
        if not "Req-Id" in field:
            Fields.append(("\"" + field + "\"" , "\"@" + field + "\""))
    node_hover_tool = HoverTool(tooltips=Fields)
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    graph_renderer = from_networkx(G, nx.spring_layout, k=3, center=(0, 0))
    graph_renderer.node_renderer.glyph = Oval(height=0.1, width=0.3, fill_color=Spectral4[0])
    #graph_renderer.node_renderer.glyph = Text(text=["@index"])
    #graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    #graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

    #graph_renderer.selection_policy = NodesAndLinkedEdges()
    #graph_renderer.inspection_policy = EdgesAndLinkedNodes()

    plot.renderers.append(graph_renderer)

    x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
    node_labels = list(G.nodes.keys())
    source = ColumnDataSource({'x': x, 'y': y,
                               'Req-Id': [node_labels[i] for i in range(len(x))]})
    labels = LabelSet(x='x', y='y', text='Req-Id', source=source,
                      background_fill_color='white')

    plot.renderers.append(labels)

    output_file("networkx_graph.html")
    show(plot)
