document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("graficoGeneral");
    if (!canvas) {
        console.error("Canvas con id 'graficoGeneral' no encontrado.");
        return;
    }

    document.getElementById("buscarVentaPorFecha").addEventListener("click", () => {
    const fecha = document.getElementById("fechaVenta").value;
    if (!fecha) {
        alert("Selecciona una fecha.");
        return;
    }

    fetch(`/venta_por_fecha/?fecha=${fecha}`)
        .then(response => response.json())
        .then(data => {
            actualizarGrafico(
                [data.fecha],  // solo una fecha
                [data.valor_total],  // solo un valor
                `Venta del ${data.fecha}`
            );
        })
        .catch(error => console.error("Error al obtener la venta por fecha:", error));
});


    const ctx = canvas.getContext("2d");
    let grafico;

    const actualizarGrafico = (etiquetas, valores, titulo) => {
        if (grafico) grafico.destroy();

        grafico = new Chart(ctx, {
            type: "bar",
            data: {
                labels: etiquetas,
                datasets: [{
                    label: titulo,
                    data: valores,
                    backgroundColor: "rgba(75, 192, 192, 0.6)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Cantidad"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Categoría"
                        }
                    }
                }
            }
        });
    };

    const obtenerDatos = () => {
        fetch("/datos_consultas/")
            .then(response => response.json())
            .then(data => {
                const mesero = document.getElementById("mesero").checked;
                const mesa = document.getElementById("mesa").checked;
                const producto = document.getElementById("producto").checked;

                const reservaMesero = document.getElementById("reservaMesero").checked;
                const reservaMesa = document.getElementById("reservaMesa").checked;
                const reservaFecha = document.getElementById("reservaFecha").checked;

                if (mesero) {
                    actualizarGrafico(
                        data.nombres_meseros,
                        data.cantidades_vendidas_meseros,
                        "Ventas por Mesero"
                    );
                } else if (mesa) {
                    actualizarGrafico(
                        data.nombres_mesas,
                        data.cantidades_vendidas_mesas,
                        "Ventas por Mesa"
                    );
                } else if (producto) {
                    actualizarGrafico(
                        data.productos,
                        data.cantidades_productos,
                        "Ventas por Producto"
                    );
                } else if (reservaMesero) {
                    actualizarGrafico(
                        data.reservas_meseros,
                        data.cantidad_reservas_meseros,
                        "Reservas por Mesero"
                    );
                } else if (reservaMesa) {
                    actualizarGrafico(
                        data.reservas_mesas,
                        data.cantidad_reservas_mesas,
                        "Reservas por Mesa"
                    );
                } else if (ventasDia) {
                    actualizarGrafico(
                        data.fechas_ventas,
                        data.valores_ventas_dias,
                        "Valor de Ventas por Día"
                    );
                } else if (reservaFecha) {
                    actualizarGrafico(
                        data.fechas_Agrupadas,
                        data.cantidad_reservas_fechas,
                        "Reservas por Fecha"
                    );
                } else {
                    alert("Selecciona al menos un filtro.");
                }
            })
            .catch(error => console.error("Error al obtener los datos:", error));
    };

    const botonActualizar = document.getElementById("actualizar");
    if (botonActualizar) {
        botonActualizar.addEventListener("click", obtenerDatos);
    } else {
        console.error("Botón con id 'actualizar' no encontrado.");
    }
});

