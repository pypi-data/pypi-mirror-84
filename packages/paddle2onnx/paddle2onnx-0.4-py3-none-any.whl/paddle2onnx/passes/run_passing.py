from paddle2onnx.passes import * 

def run_passing(graph, custom_pass_list=[], verbose=False):
    for pass_name in custom_pass_list:
        graph = eval(pass_name)(graph)
    return graph


