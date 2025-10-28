import React from "react";
import { Bar } from "react-chartjs-2";
import "./VisualizationArea.css";

export default function VisualizationArea({ data }) {
  if (!data) return null;

  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: data.label,
        data: data.values,
        backgroundColor: "rgba(0, 123, 255, 0.6)",
      },
    ],
  };

  return (
    <div className="visualization">
      <h3>{data.title}</h3>
      <Bar data={chartData} />
    </div>
  );
}
