import mysql.connector

def get_connection():
    connection = mysql.connector.connect(host='localhost',
                                         database='chat_server_sistemas_distribuidos',
                                         user='root',
                                         password='')
    return connection

def close_connection(connection):
    if connection:
        connection.close()

def registrar_usuario(nombre, edad, contrasena, genero, nombre_usuario, imagen=None):
    '''
    Registra los datos del usuario que se añada a la base de datos

    Parametros
    --------------------------
    nombre, edad, contrasena, genero, nombre_usuario

    La imagen esta dada como nula en caso que no se agregue

    Retorna
    --------------------------
    Nada
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        if imagen == None:
            sql = ''' 
            INSERT INTO usuarios (nombre_completo, edad, contrasena, genero, nombre_usuario)
            VALUES
            (%s, %s, %s, %s, %s)
            '''
        else:
            sql = ''' 
            INSERT INTO usuarios (nombre_completo, edad, contrasena, genero, imagen_perfil, nombre_usuario)
            VALUES
            (%s, %s, %s, %s, %s)
            '''
        cursor.execute(sql, (nombre, edad, contrasena, genero, nombre_usuario))
        connection.commit()
        close_connection(connection)
    except (Exception, mysql.connector.Error) as error:
        print(error)


def registrar_grupo(nombre, nombre_usuario_admin):
    '''
    Registra los datos de un grupo que se añada a la base de datos

    Parametros
    --------------------------
    nombre, nombre_usuario_admin

    Retorna
    --------------------------
    Nada
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = ''' 
        INSERT INTO grupos (nombre_grupo, nombre_usuario_admin)
        VALUES
        (%s, %s)
        '''
        cursor.execute(sql, (nombre, nombre_usuario_admin))
        connection.commit()
        close_connection(connection)
    except (Exception, mysql.connector.Error) as error:
        print(error)


def registrar_grupo_usuario(id_grupo, nombre_usuario):
    '''
    Registra el id de un grupo, junto a un usuario dentro del grupo, para poder tener
    registro de todos los grupos a los que pertenece dicho usuario

    Parametros
    --------------------------
    id_grupo, nombre_usuario

    Retorna
    --------------------------
    Nada
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = ''' 
        INSERT INTO grupos_usuario (id_grupo, nombre_usuario)
        VALUES
        (%s, %s)
        '''
        cursor.execute(sql, (id_grupo, nombre_usuario))
        connection.commit()
        close_connection(connection)
    except (Exception, mysql.connector.Error) as error:
        print(error)

def registrar_mensaje(nombre_usuario, id_grupo, mensaje):
    '''
    registra los datos de un mensaje enviado, el texto, el usuario y el grupo al que se mandó

    Parametros
    --------------------------
    nombre_usuario, id_grupo, mensaje

    Retorna
    --------------------------
    Nada
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = ''' 
        INSERT INTO mensajes (nombre_usuario, id_grupo, mensaje)
        VALUES
        (%s, %s, %s)
        '''
        cursor.execute(sql, (nombre_usuario, id_grupo, mensaje))
        connection.commit()
        close_connection(connection)
    except (Exception, mysql.connector.Error) as error:
        print(error)

def validar_usuario(nombre_usuario, contrasena):
    '''
    Valida la existencia de un usuario dentro de la base de datos

    Parametros
    --------------------------
    nombre_usuario, contrasena

    Retorna
    --------------------------
    
    Debe retornar una tupla con los datos del usuario si existe
    Ej: ('Nombre completo', Edad, 'contraseña', 'Género', 'Nombre de usuario')
    En caso de no existir debe retornar:  None
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = ''' 
        SELECT nombre_completo, edad, contrasena, genero, nombre_usuario FROM usuarios 
        WHERE nombre_usuario = %s and contrasena = %s
        '''
        cursor.execute(sql, (nombre_usuario, contrasena))
        data = cursor.fetchone()
        close_connection(connection)
        return data
    except (Exception, mysql.connector.Error) as error:
        print(error)

def seleccionar_id_grupos_por_usuario(nombre_usuario):
    '''
    Selecciona los id de grupos a los que pertenece un usuario en particular

    Parametros
    --------------------------
    nombre_usuario

    Retorna
    --------------------------
    
    Debe retornar una lista con los id de grupos a los que pertenece
    Ej: [1,2,6,105]
    En caso de no existir grupo debe retornar:  None
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = ''' 
        SELECT id_grupo FROM grupos_usuario WHERE nombre_usuario = %s
        '''
        cursor.execute(sql, (nombre_usuario,))
        data = cursor.fetchall()
        data = [id[0] for id in data]
        close_connection(connection)
        return data
    except (Exception, mysql.connector.Error) as error:
        print(error)

def seleccionar_grupo_por_id(id_grupo):
    '''
    Selecciona el nombre de un grupo por su id

    Parametros
    --------------------------
    id_grupo

    Retorna
    --------------------------
    
    Debe retornarun string con el nombre del grupo
    Ej: 'nombre_grupo'
    En caso de no existir grupo debe retornar:  None
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = ''' 
        SELECT nombre_grupo FROM grupos 
        WHERE id = %s
        '''
        cursor.execute(sql, (id_grupo,))
        data = cursor.fetchone()
        close_connection(connection)
        return data[0]
    except (Exception, mysql.connector.Error) as error:
        print(error)

def retornar_grupos_usuario(nombre_usuario):
    '''
    Combina las funciones seleccionar_id_grupos_por_usuario y 
    seleccionar_grupo_por_id para devolver una lista
    con los nombres de los grupos a los cuales pertenece

    Parametros
    --------------------------
    nombre_usuario

    Retorna
    --------------------------
    
    Debe retornar una lista con los nombres de los grupos a los que pertenece
    Ej: ['nombre_grupo1', 'nombre_grupo2', 'nombre_grupon']
    En caso de no existir grupo debe retornar:  None
    '''
    data = seleccionar_id_grupos_por_usuario(nombre_usuario)
    data = [seleccionar_grupo_por_id(id) for id in data]
    return data

def seleccionar_mesajes_grupo(id_grupo):
    '''
    Selecciona los mensajes de un grupo en particular

    Parametros
    --------------------------
    id_grupo

    Retorna
    --------------------------
    
    Debe retornar una lista en la cual contiene tuplas que a su vez contienen el nombre de usuario y el mensaje
    Ej: [('usuario1', ('Hola')), ('usuario2', ('Hola'))]
    En caso de no existir debe retornar:  None
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = ''' 
        SELECT nombre_usuario, mensaje FROM mensajes 
        WHERE id_grupo = %s
        '''
        cursor.execute(sql, (id_grupo,))
        data = cursor.fetchall()
        close_connection(connection)
        return data
    except (Exception, mysql.connector.Error) as error:
        print(error)