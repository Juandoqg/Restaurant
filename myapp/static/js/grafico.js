document.addEventListener("DOMContentLoaded", function() {
  // Hacer la solicitud fetch al endpoint datos_facturas
  fetch('/datos_facturas/')
    .then(response => response.json()) // Parsear la respuesta como JSON
    .then(data => {
      // Verificar los datos
      console.log("Datos recibidos:", data);
      
      // Obtener fechas y valores de la respuesta
      const fechas = data.fechas;
      const valores = data.valores;

      // Llamar a la función para crear el gráfico con los datos obtenidos
      crearGrafico(fechas, valores);
    })
    .catch(error => {
      console.error("Error al obtener los datos:", error);
    });
});

const crearGrafico = (fechas, valores) => {
  const ctx = document.getElementById('histograma').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'line', // Tipo de gráfico
    data: {
      labels: fechas, // Las fechas se pasan como etiquetas en el eje X
      datasets: [{
        label: 'Total venta del dia',
        data: valores, // Los valores asociados a cada fecha
        backgroundColor: 'rgba(54, 162, 235, 1)', // Color de las barras (sólido, no transparente)
        borderColor: 'rgba(54, 162, 235, 1)', // Color del borde de las barras
        borderWidth: 1
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
      // Fondo blanco para la zona de las barras y cuadrículas
      backgroundColor: '#ffffff', // Fondo blanco para el gráfico
      elements: {
        bar: {
          backgroundColor: 'rgba(54, 162, 235, 1)' // Aseguramos que las barras sean de color sólido
        }
      }
    }
  });
};
