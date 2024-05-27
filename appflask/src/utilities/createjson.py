def productosJson(data):
    arreglo = []
    for i in data :
        temp_list = {}
        temp_list['id'] = int(i[0])
        temp_list['nombre'] = i[1]
        temp_list['valor'] = int(i[2])
        temp_list['stock'] = int(i[3])
        arreglo.append(temp_list)
    return arreglo





