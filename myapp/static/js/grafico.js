document.addEventListener("DOMContentLoaded", function() {
  // Hacer la solicitud fetch al endpoint datos_facturas
  fetch('/datos_facturas/')
    .then(response => response.json()) // Parsear la respuesta como JSON
    .then(data => {
      // Verificar los datos
      console.log("Datos recibidos:", data);
    

      
      // Obtener las fechas y valores de la respuesta
      const fechas = data.fechas;
      const valores = data.valores;
      // datos mesero grafico
      const meseros = data.nombres_meseros;
      const ventas = data.cantidades_vendidas_meseros
      // datos mesa grafico
      const mesas = data.nombres_mesas
      

      // Agrupar las facturas por fecha y sumar los valores
      const fechasAgrupadas = [];
      const valoresSumados = [];
      const ventas_mesas = data.cantidades_vendidas_mesas; // Asegúrate de que esta variable esté definida correctamente
let total_venta_mesas = 0; // Inicializamos el total en 0

ventas_mesas.forEach(cantidad => {
  total_venta_mesas += cantidad;  // Sumamos cada valor al total
});

console.log('Total venta mesas:', total_venta_mesas);

      // Crear un objeto para almacenar las fechas únicas y sus valores sumados
      const sumaPorFecha = {};

      // Agrupar por fecha
      fechas.forEach((fecha, index) => {
        if (sumaPorFecha[fecha]) {
          sumaPorFecha[fecha] += valores[index]; // Sumar el valor de las facturas del mismo día
        } else {
          sumaPorFecha[fecha] = valores[index]; // Crear una nueva entrada para la fecha
        }
      });

      // Convertir el objeto de fechas agrupadas a arreglos para las etiquetas y valores del gráfico
      for (const fecha in sumaPorFecha) {
        fechasAgrupadas.push(fecha);
        valoresSumados.push(sumaPorFecha[fecha]);
      }

      // Llamar a la función para crear el gráfico con los datos agrupados
      crearGrafico(fechasAgrupadas, valoresSumados);
      crearGrafico2(meseros,ventas);
      crearGrafico3(mesas, ventas_mesas, total_venta_mesas);
    })
    .catch(error => {
      console.error("Error al obtener los datos:", error);
    });
});

const crearGrafico = (fechas, valores) => {
  const ctx = document.getElementById('histograma').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar', // Cambiar el tipo de gráfico a 'bar' (barras)
    data: {
      labels: fechas, // Las fechas se pasan como etiquetas en el eje X
      datasets: [{
        label: 'Total venta del día',
        data: valores, // Los valores sumados para cada fecha
        backgroundColor: 'rgba(255, 165, 0, 0.6)', // Color naranja con opacidad de las barras
        borderColor: 'rgba(255, 165, 0, 0.6)', // Color del borde de las barras (azul)
        borderWidth: 1, // Ancho del borde de las barras
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            font: {
              family: 'Arial',
              size: 14
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: 'black' // Color de los ticks del eje Y
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje Y
          },
          title: {
            display: true,
            text: 'Cantidad', // Título del eje Y
            color: 'black', // Color del título del eje Y
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        },
        x: {
          ticks: {
            color: 'black' // Color de los ticks del eje X
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje X
          },
          title: {
            display: true,
            text: 'Día', // Título del eje X
            color: 'black', // Color del título del eje X
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        }
      },
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      backgroundColor: '#ffffff', // Fondo blanco para el gráfico
    }
  });
};


const crearGrafico2 = (nombres, ventas) => {
  const ctx = document.getElementById('meseros').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar', // Tipo de gráfico: Barras
    data: {
      labels: nombres, // Las etiquetas serán los nombres de los meseros
      datasets: [{
        label: 'Venta de meseros',
        data: ventas, // Las ventas totales por mesero
        backgroundColor: 'rgba(255, 165, 0, 0.6)', // Color naranja con opacidad de las barras
        borderColor: 'rgba(255, 165, 0, 0.6)', // Color del borde de las barras (azul)
        borderWidth: 1, // Ancho del borde de las barras
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top', // Posición de la leyenda
          labels: {
            font: {
              family: 'Arial', // Tipo de fuente para la leyenda
              size: 14 // Tamaño de la fuente
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: 'black' // Color de los ticks del eje Y
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje Y
          },
          title: {
            display: true,
            text: 'Cantidad', // Título del eje Y
            color: 'black', // Color del título del eje Y
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        },
        x: {
          ticks: {
            color: 'black' // Color de los ticks del eje X
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje X
          },
          title: {
            display: true,
            text: 'Nombre de usuario', // Título del eje X
            color: 'black', // Color del título del eje X
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        }
      },
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      backgroundColor: '#ffffff', // Fondo blanco para el gráfico
    }
  });
};


const crearGrafico3 = (mesas, ventas_mesas, total_venta_mesas) => {
  const ctx = document.getElementById('mesas').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'pie', // Tipo de gráfico: Torta
    data: {
      labels: mesas, // Las mesas se pasan como etiquetas en el gráfico
      datasets: [{
        label: 'Total venta por mesa',
        data: ventas_mesas, // Los valores sumados para cada mesa
        backgroundColor: [
          'rgba(54, 162, 235, 1)', // Color para la primera sección
          'rgba(255, 99, 132, 1)', // Color para la segunda sección
          'rgba(255, 159, 64, 1)', // Color para la tercera sección
          'rgba(75, 192, 192, 1)', // Color para la cuarta sección
          'rgba(153, 102, 255, 1)', // Color para la quinta sección
          'rgba(255, 159, 64, 1)', // Color para más secciones
          'rgba(255, 205, 86, 1)'  // Otro color si hay más mesas
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)', // Color de borde para la primera sección
          'rgba(255, 99, 132, 1)', // Color de borde para la segunda sección
          'rgba(255, 159, 64, 1)', // Color de borde para la tercera sección
          'rgba(75, 192, 192, 1)', // Color de borde para la cuarta sección
          'rgba(153, 102, 255, 1)', // Color de borde para la quinta sección
          'rgba(255, 159, 64, 1)', // Color de borde para más secciones
          'rgba(255, 205, 86, 1)'  // Otro color de borde
        ],
        borderWidth: 1, // Ancho del borde de las secciones
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top', // Posición de la leyenda
          labels: {
            font: {
              family: 'Arial',
              size: 14
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return `${tooltipItem.label}: ${tooltipItem.raw}`; // Formato de la etiqueta en el tooltip
            }
          }
        },
        title: {
          display: true, // Habilitar el título
          text: `Ventas de mesas x productos: ${total_venta_mesas}`, // Título dinámico con el valor de total_venta_mesas
          font: {
            size: 18, // Tamaño de la fuente del título
            family: 'Arial', // Tipo de fuente
            weight: 'bold' // Peso de la fuente
          },
          color: '#333', // Color del título
          padding: {
            top: 10,    // Espacio superior
            bottom: 20  // Espacio inferior
          }
        }
      },
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      cutoutPercentage: 0, // Esto asegura que sea un gráfico de torta completo (sin agujero en el medio)
      backgroundColor: '#ffffff', // Fondo blanco para el gráfico
    }
  });
};
