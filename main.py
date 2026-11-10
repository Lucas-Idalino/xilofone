from persistencia import PersistenciaJSON
from inventario import Inventario
from app import AppInventario


def main():
    persistencia = PersistenciaJSON("base_inventario.json")
    inventario = Inventario(persistencia)
    app = AppInventario(inventario)
    app.executar()


if __name__ == "__main__":
    main()