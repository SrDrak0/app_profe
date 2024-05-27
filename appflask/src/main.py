from flask import Flask,render_template ,request
from utilities.condb import condb
from utilities.createjson import productosJson
from datetime import date


app = Flask(__name__)

def productos():    
    cursor = condb.cursor()
    query = "SELECT * FROM productos"
    cursor.execute(query)
    productos = cursor.fetchall()
    cursor.close()
    return productos

def clientes():    
    cursor = condb.cursor()
    query = "SELECT * FROM clientes"
    cursor.execute(query)
    clientes = cursor.fetchall()
    cursor.close()
    return clientes

def comprasTotales():    
    cursor = condb.cursor()
    query = "SELECT * FROM compras ;"
    cursor.execute(query)
    compras = cursor.fetchall()
    cursor.close()
    return compras

def actulizarStock(datos):    
    cursor = condb.cursor()
    query = "UPDATE productos SET stock = %s WHERE id_producto = %s;"
    cursor.executemany(query, datos)
    condb.commit()
    cursor.close()
    return "Actaulzados con exito"

def ingresarCliente(id,name):    
    cursor = condb.cursor()
    query = "SELECT id_cliente FROM clientes  WHERE id_cliente = %s;"
    cursor.execute(query,(id,))
    result = cursor.fetchone()    
    if result != None:
        cursor.close()
    else:
        query = "INSERT INTO clientes (id_cliente, nombre ) VALUES (%s,%s)"
        cursor.execute(query,(id,name))
        condb.commit()
        cursor.close()
        return "Actaulzados con exito"""

def ingresarCompra(id,fecha,total):    
    cursor = condb.cursor()
    query = "INSERT INTO compras (id_cliente, fecha_compra, total) VALUES (%s,%s,%s)"
    cursor.execute(query,(id,fecha, total))
    condb.commit()
    cursor.execute("SELECT LAST_INSERT_ID();")
    id_generado = cursor.fetchone()
    
    cursor.close()
    return id_generado

def insertarCompras_productos(datos):    
    cursor = condb.cursor()
    query = "INSERT INTO compras_productos (id_compra, id_producto, cantidad, precio_unitario) VALUES (%s,%s,%s,%s)"
    cursor.executemany(query, datos)
    condb.commit()
    cursor.close()
    return "Actaulzados con exito"


@app.route("/", methods=['GET','POST'])
def compras():
    products = productos()
    productos_ = productosJson(products)
    if request.method =='POST':
        data =  request.form
        reaorganizado = list(data.items())
        subarrays = [reaorganizado[i:i+5] for i in range(0, len(reaorganizado), 5)]
        datos_cliente = subarrays[-1]
        subarrays.pop()
        items = []
        stock_nuevo = []
        print(datos_cliente)
        for arreglo in subarrays:
            segundos_valores = []
            for tupla in arreglo:   
                segundos_valores.append(tupla[1])
            items.append(segundos_valores)

        data_client = []
        for i in datos_cliente:
            segundos_valores = []
            data_client.append(i[1])
        id_c = int(data_client[0])
        name_c = str(data_client[1])
        fecha_actual = date.today()
        total = int(data_client[2])

        ingresarCliente(id_c,name_c)

        id_generado = ingresarCompra(id_c,fecha_actual,total)
        id_generado = id_generado[0]

        for i in items:
            del i[1]
            del i[3]
            i.insert(0, int(id_generado))
            print(i)
            data_stock = []
            data_stock.append(i[2]) 
            data_stock.append(int(i[0]))         
            stock_nuevo.append(data_stock)
        

        for j in stock_nuevo:
            for i in products:
                if j[1] == i[0]:
                    stock = int(i[3]) - int(j[0])
                    j[0] = stock
        
        actulizarStock(stock_nuevo)

        insertarCompras_productos(items)
        
        return " Compra realizada satisfactoriamente "
    return render_template('main.html', chart_data=productos_)

@app.route("/clientes", methods=['GET','POST'])
def clientesVista():
    clientes_ = clientes()
    return render_template('clientes.html', clientes=clientes_)

@app.route("/compras", methods=['GET','POST'])
def comprastabla():
    comprasTotales_ = comprasTotales()
    return render_template('compras.html', comprasTotales=comprasTotales_)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


