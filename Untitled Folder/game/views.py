from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from .utils import Graph


def index(request):
    graph_id = request.session.get('game_id', None)

    graph = Graph()
    if graph_id:
        graph.clear()
        graph.load(graph_id)
        if not graph.error_msg:
            if request.is_ajax():
                data = request.POST
                type = data.get('type')
                pos_x = int(data.get('x')) if data.get('x') else None
                pos_y = int(data.get('y')) if data.get('y') else None

                if type == 'row':
                    neighbour_pos_x = pos_x
                    neighbour_pos_y = pos_y + 2
                else:
                    neighbour_pos_x = pos_x + 2
                    neighbour_pos_y = pos_y
                print(pos_x, pos_y, neighbour_pos_x, neighbour_pos_y)
                graph.addedge_by_pos(pos_x, pos_y, neighbour_pos_x, neighbour_pos_y)
                graph.save(graph.id)
        else:
            request.session['game_id'] = None
    else:
        request.session['game_id'] = graph.id

    graph.save(graph.id)
    response = render(request, 'index.html', context={'graph': graph})
    response['game_id ID'] = graph.id
    return response
