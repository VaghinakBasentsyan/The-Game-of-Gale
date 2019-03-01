from django import template

register = template.Library()


@register.filter('cell_range')
def cell_range(num):
    return range(0, num)

@register.filter('is_even')
def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False

@register.simple_tag()
def is_checked(graph, pos_x, pos_y, type):
    if type == 'row':
        neighbour_pos_x = pos_x
        neighbour_pos_y = pos_y + 2
    else:
        neighbour_pos_x = pos_x + 2
        neighbour_pos_y = pos_y
    node_1 = graph.find_node_by_pos(pos_x, pos_y)
    node_2 = graph.find_node_by_pos(neighbour_pos_x, neighbour_pos_y)

    return graph.has_edge(node_1.id, node_2.id) if node_1 and node_2 else False
