from django.http import HttpResponse
from django.shortcuts import render, redirect
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

                if graph.add_edge_by_pos(pos_x, pos_y, neighbour_pos_x, neighbour_pos_y):
                    graph.which_next = 'red' if graph.which_next=='blue' else 'blue'
                if graph.is_over():
                    graph.error_msg = "Game Over"
                graph.save(graph.id)
        else:
            request.session['game_id'] = None
    else:
        request.session['game_id'] = graph.id
    graph.save(graph.id)
    response = render(request, 'index.html', context={'graph': graph, 'CELL_HEIGHT': 11, 'CELL_WEIGHT': 11, 'msg': graph.error_msg})
    response['game_id ID'] = graph.id
    return response


def new_game(request):
    request.session['game_id'] = None
    return redirect('/')
