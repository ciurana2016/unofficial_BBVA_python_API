# API no oficial BBVA

La web del bbva tarda demasiado en cargar, si eres programador ahora puedes consultar tu banco en un instante desde la terminal con esta API no oficial. (ya que la oficial es solo para empresas y de pago)

### Tests
Para que los tests funcionen se han de crear las siguientes variables de sistema para hacer el login:
```
B_AC=DNI
B_AP=PASS
```

Hay un test con **skip** ya que el servidor renueva un header esencial cada 4 minutos, pero el test lo pasa ok.

### Ejemplo de uso
```
python api.py
```

### Por hacer
Demasiadas cosas.
