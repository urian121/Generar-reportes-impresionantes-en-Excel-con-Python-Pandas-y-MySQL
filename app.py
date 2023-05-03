import pandas as pd
import mysql.connector
import openpyxl


def connectionBD():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="demo",
            raise_on_warnings=True
        )
        if connection.is_connected():
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")


# Funcion para realizar la consulta a BD y generar el reporte en Excel
def reporteExcelBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = """SELECT * FROM personas"""
                mycursor.execute(querySQL,)
                dataBD = mycursor.fetchall()

                # creando un nuevo objeto de libro de trabajo de Excel usando la biblioteca de Python openpyxl
                wb = openpyxl.Workbook()

                ''' 
                wb.active, se refiere a la hoja activa del libro de trabajo de Excel. Es decir
                es la hoja de trabajo en la que se insertarán los datos en primer lugar cuando se utilice la instancia hoja
                '''
                hoja = wb.active
                # Crea la fila del encabezado con los títulos
                hoja.append(('N° Registro', 'Usuario', 'Nombre', 'Sexo', 'Email', 'Telefono', 'Compañia'))
                for filaPersona in dataBD:
                    # Agrega una tupla con los valores de la consignación
                    hoja.append((filaPersona['id_persona'], filaPersona['usuario'],
                                filaPersona['nombre'], filaPersona['sexo'], filaPersona['email'], filaPersona['telefono'], filaPersona['company']))

                # Guarda el archivo Excel
                wb.save('mi_DataBD.xlsx')

    except Exception as e:
        print(f"Ocurrió un error leyendo la consignación: {e}")
        return {}


if __name__ == '__main__':
    reporteExcelBD()
