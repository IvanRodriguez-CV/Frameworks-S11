from django.test import TestCase
from django.utils import timezone

from .models import Categoria, Cliente, Rol, TipoPago


class CategoriaTests(TestCase):
    def test_lista_sin_categorias_se_muestra(self):
        respuesta = self.client.get("/categoria/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(respuesta.context["categorias"])

    def test_categoria_se_guarda_y_se_muestra_en_la_lista(self):
        ahora = timezone.now()
        categoria = Categoria.objects.create(
            nombre="Electrónicos",
            descripcion="Productos electrónicos",
            created_at=ahora,
            updated_at=ahora,
        )

        respuesta = self.client.get("/categoria/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Electrónicos")
        self.assertContains(respuesta, str(categoria.id))
        self.assertIn(categoria, respuesta.context["categorias"])

    def test_str_incluye_nombre_y_datos_del_registro(self):
        ahora = timezone.now()
        categoria = Categoria.objects.create(
            nombre="Libros",
            descripcion="Libros de práctica",
            created_at=ahora,
            updated_at=ahora,
        )

        self.assertIn("Libros", str(categoria))
        self.assertIn("Id:", str(categoria))


class ModelosDeTareasTests(TestCase):
    def test_tipos_de_pago_clientes_y_roles_se_guardan(self):
        tipo_pago = TipoPago.objects.create(nombre="Tarjeta")
        cliente = Cliente.objects.create(
            nombres="Ana",
            apellidos="Pérez",
            email="ana@example.com",
        )
        rol = Rol.objects.create(nombre="Administrador")

        self.assertEqual(TipoPago.objects.get(pk=tipo_pago.pk).nombre, "Tarjeta")
        self.assertEqual(str(cliente), "Ana Pérez")
        self.assertEqual(Rol.objects.get(pk=rol.pk).nombre, "Administrador")
