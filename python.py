from  fasr


segurity = HTTPBasic

def verificar_Peticion(credenciales: HTTPBasicCredentials=Depends(segurity)):
    usuarioAuth = secrets.compare_digest(credenciales.username,"admin")
    usuarioAuth = secrets.compare_digest(credenciales.password,"123456789")

    if not(usuarioAuth and contraAuth):
        raise HTTPExcepcion(
            status_code = status.HTTP_401_UNAUTHORIZED
            details ="Creden no validas"
        )
    
    return credentials.username