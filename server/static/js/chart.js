window.onload = async () => {
  const response = await fetch("/chart/courses");
  const data = await response.json();

  const ctx = document.getElementById("statsChart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: data.labels,
      datasets: data.datasets.map((ds) => ({
        label: ds.label,
        data: ds.data,
        fill: false,
        backgroundColor: ds.backgroundColor,
        borderColor: ds.borderColor,
        tension: 0.1,
      })),
    },
  });
};