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

      const meseros = data.nombres_meseros;
      const ventas = data.cantidades_vendidas_meseros

      // Agrupar las facturas por fecha y sumar los valores
      const fechasAgrupadas = [];
      const valoresSumados = [];

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
        backgroundColor: 'rgba(54, 162, 235, 0.6)', // Color de las barras (azul con opacidad)
        borderColor: 'rgba(54, 162, 235, 1)', // Color del borde de las barras (azul)
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
          }
        },
        x: {
          ticks: {
            color: 'black' // Color de los ticks del eje X
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje X
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
        backgroundColor: 'rgba(54, 162, 235, 0.6)', // Color azul con opacidad de las barras
        borderColor: 'rgba(54, 162, 235, 1)', // Color del borde de las barras (azul)
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
          beginAtZero: true, // Asegura que el eje Y comience en cero
          ticks: {
            color: 'black' // Color de los números en el eje Y
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de las líneas de la cuadrícula en el eje Y
          }
        },
        x: {
          ticks: {
            color: 'black' // Color de los números en el eje X
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de las líneas de la cuadrícula en el eje X
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

