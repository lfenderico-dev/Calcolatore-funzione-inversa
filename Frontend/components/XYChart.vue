<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const props = defineProps({
  xData: {
    type: Array as () => (number | null)[],
    required: true,
    default: () => [],
  },
  yData: {
    type: Array as () => (number | null)[],
    required: true,
    default: () => [],
  },
  label: {
    type: String,
    default: "Dati",
  },
});

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

// Funzione per ottenere il colore primario dal CSS
const getPrimaryColor = () => {
  if (typeof window === "undefined") return "rgb(75, 192, 192)";

  const root = document.documentElement;
  const primaryColor = getComputedStyle(root)
    .getPropertyValue("--color-primary-500")
    .trim();

  // Se il colore è vuoto o non trovato, usa un fallback
  return primaryColor || "rgb(99, 102, 241)"; // Indigo-500 come fallback
};

const createChart = () => {
  if (chartInstance) {
    chartInstance.destroy();
  }

  if (!chartCanvas.value) return;

  const ctx = chartCanvas.value.getContext("2d");
  if (!ctx) return;

  const primaryColor = getPrimaryColor();

  // Converti gli array in formato {x, y} e filtra valori undefined
  const dataPoints = props.xData
    .map((x, i) => ({
      x: x,
      y: props.yData[i],
    }))
    .filter(
      (point): point is { x: number; y: number } =>
        point.x !== undefined && point.y !== undefined
    );

  chartInstance = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: props.label,
          data: dataPoints,
          backgroundColor: primaryColor,
          borderColor: primaryColor,
          showLine: true,
          tension: 0.1,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
      },
      scales: {
        x: {
          type: "linear",
          position: "center",
          title: {
            display: true,
            text: "X",
          },
          grid: {
            color: (context) => {
              if (context.tick.value === 0) {
                return "rgba(0, 0, 0, 0.8)";
              }
              return "rgba(0, 0, 0, 0.1)";
            },
            lineWidth: (context) => {
              if (context.tick.value === 0) {
                return 2;
              }
              return 1;
            },
          },
          ticks: {
            callback: function (value) {
              return value;
            },
          },
        },
        y: {
          type: "linear",
          position: "center",
          title: {
            display: true,
            text: "Y",
          },
          grid: {
            color: (context) => {
              if (context.tick.value === 0) {
                return "rgba(0, 0, 0, 0.8)";
              }
              return "rgba(0, 0, 0, 0.1)";
            },
            lineWidth: (context) => {
              if (context.tick.value === 0) {
                return 2;
              }
              return 1;
            },
          },
        },
      },
    },
  });
};

onMounted(() => {
  createChart();
});

watch(
  () => [props.xData, props.yData],
  () => {
    createChart();
  },
  { deep: true }
);

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: auto;
}
</style>
