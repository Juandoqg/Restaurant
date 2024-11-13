from django.urls import path
from .views import views
from .views import viewsUser
from .views import viewsMesa
from .views import viewsProducto
from .views import viewsPedido
from .views import viewsFactura

urlpatterns = [
     path('',views.signin, name = "signin"),
     path('administrador/', views.administrador, name="administrador"),
     path('datos_facturas/', viewsFactura.datos_facturas, name="datos_facturas"),
     path('verMesas/', viewsMesa.verMesas, name = "verMesas"),
     path('chef/', views.chef, name = "chef"),
     path('signout/', views.signout, name='signout'),
     path('createUser/', views.createUser, name='createUser'),
     path("showUsers/",viewsUser.showUsers, name ="showUsers"),
     path("listUsers/",viewsUser.listUsers, name = "listUsers"),
      path("listUserPorId/<int:user_id>",viewsUser.listUserPorId, name = "listUsersPorId"),
     path("listMesas/",viewsMesa.listMesas, name = "listMesas"),
     path("listMesasPorId/<int:idMesa>",viewsMesa.listMesasPorId, name = "listMesasPorId"),
     path("listProductos/",viewsProducto.listProductos, name = "listProductos"),
     path("deleteUser/<int:user_id>/",viewsUser.deleteUser, name ="deleteUser"),
     path("actulizarDatosUsuario/<int:user_id>/",viewsUser.actualizarDatosUsuario,name="actulizarDatosUsuario"),
     path('createProduct/', viewsProducto.createProduct, name='createProduct'),
     path('tomarPedido/<int:idMesa>', viewsPedido.tomarPedido, name='tomarPedido'),
     path('savePedido/<int:idMesa>', viewsPedido.savePedido, name='savePedido'),
     path('verPedido/<int:idMesa>/', viewsPedido.verPedido, name='verPedido'),
     path('showProduct/', viewsProducto.showProduct, name='showProduct'),
     path('cambiar_estado_pedido/<int:pedido_id>/', viewsPedido.cambiar_estado_pedido, name='cambiar_estado_pedido'),
     path('verFacturaID/<int:idMesa>/', viewsFactura.verFacturaID, name='verFacturaID'),
     path('verFactura/', viewsFactura.verFactura, name='verFactura'),
     path('crearMesas/', viewsMesa.crearMesas, name='crearMesas'),
     path('recuperarContra/', viewsUser.recuperarContra, name='recuperarContra'),
     path('actualizarContra/', viewsUser.actualizarContra, name='actualizarContra'),
     path('borrarPedido/<int:idMesa>/', viewsPedido.borrarPedido, name='borrarPedido')
] 