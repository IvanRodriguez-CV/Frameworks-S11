from decimal import Decimal
from io import BytesIO
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone
from PIL import Image

from .models import Categoria, Cliente, Producto, Rol, TipoPago


class CategoriaTests(TestCase):
    def test_categorias_de_ejemplo_se_crean_con_la_migracion(self):
        self.assertTrue(
            Categoria.objects.filter(
                nombre="tv",
                descripcion="Televisores de alta gama",
            ).exists()
        )
        self.assertTrue(
            Categoria.objects.filter(
                nombre="Laptop",
                descripcion="Computadoras portátiles",
            ).exists()
        )

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
        self.assertContains(respuesta, "Productos electrónicos")
        self.assertIn(categoria, respuesta.context["categorias"])

    def test_lista_vacia_se_muestra_sin_error(self):
        Categoria.objects.all().delete()
        respuesta = self.client.get("/categoria/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Aún no hay categorías registradas.")

    def test_str_incluye_nombre_y_datos_del_registro(self):
        ahora = timezone.now()
        categoria = Categoria.objects.create(
            nombre="Libros",
            descripcion="Libros de práctica",
            created_at=ahora,
            updated_at=ahora,
        )

        self.assertIn("Libros", str(categoria))
        self.assertIn("id:", str(categoria))

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


class ProductoTests(TestCase):
    def test_categoria_se_relaciona_con_producto_y_lo_elimina_en_cascada(self):
        categoria = Categoria.objects.create(
            nombre="Televisores",
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        image_buffer = BytesIO()
        Image.new("RGB", (1, 1)).save(image_buffer, format="PNG")

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                producto = Producto.objects.create(
                    nombre="Televisor",
                    descripcion="Televisor de prueba",
                    precio=Decimal("349.99"),
                    stock=3,
                    imagen=SimpleUploadedFile(
                        "televisor.png",
                        image_buffer.getvalue(),
                        content_type="image/png",
                    ),
                    categoria=categoria,
                )

                self.assertEqual(producto.categoria, categoria)
                self.assertEqual(list(categoria.productos.all()), [producto])
                self.assertTrue(producto.imagen.name.startswith("productos/"))
                self.assertEqual(str(producto), "Televisor")

                categoria.delete()

                self.assertFalse(Producto.objects.filter(pk=producto.pk).exists())

                producto.imagen.delete(save=False)
