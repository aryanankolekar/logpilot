import React, { useState, useEffect } from "react";
import { Bar, Line, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend,
  TimeScale,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend,
  TimeScale
);

export default function VisualizationPanel({ query }) {
  const [stats, setStats] = useState(null);
  const [highlight, setHighlight] = useState({
    severity: false,
    timeline: false,
    pods: false,
    components: false,
    security: false,
  });

  // 🔁 Fetch data every 5 s
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch("/api/stats");
        const data = await res.json();
        setStats(data);
      } catch (err) {
        console.error("Stats fetch failed", err);
      }
    };
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  // 💡 Highlight relevant panels by query keywords
  useEffect(() => {
    if (!query) return;
    const q = query.toLowerCase();
    setHighlight({
      severity: /error|severity|crash/.test(q),
      timeline: /trend|timeline|hour|day|24/.test(q),
      pods: /pod|inference|latency|timeout|oom/.test(q),
      components: /load|traffic|component|distribution/.test(q),
      security: /auth|token|login|network|timeout|gateway/.test(q),
    });
    const timer = setTimeout(
      () =>
        setHighlight({
          severity: false,
          timeline: false,
          pods: false,
          components: false,
          security: false,
        }),
      10000
    );
    return () => clearTimeout(timer);
  }, [query]);

  if (!stats)
    return (
      <div className="viz-body">
        <p>Loading visualizations...</p>
      </div>
    );

  // Defensive destructuring with default values
  const {
    severity_counts = {},
    timeline = [],
    pod_performance = {},
    errors_by_component = {},
    auth_fails = 0,
    network_timeouts = 0,
  } = stats || {};

  // Chart 1 – Severity Breakdown
  const severityData = {
    labels: Object.keys(severity_counts),
    datasets: [
      {
        data: Object.values(severity_counts),
        backgroundColor: ["#cce5ff", "#ffeeba", "#f5c6cb", "#f8d7da"],
      },
    ],
  };

  // Chart 2 – Error Timeline
  const timelineData = {
    labels: timeline.map((t) => t.timestamp.slice(11, 16)),
    datasets: [
      {
        label: "Errors",
        data: timeline.map((t) => t.errors),
        fill: true,
        borderColor: "#0078ff",
        tension: 0.3,
      },
    ],
  };

  // Chart 3 – Pod Performance
  const podNames = Object.keys(pod_performance);
  const podLatency = podNames.map((p) => pod_performance[p].latency_avg_ms);
  const podTimeouts = podNames.map((p) => pod_performance[p].timeouts);

  const podData = {
    labels: podNames,
    datasets: [
      {
        label: "Avg Latency (ms)",
        data: podLatency,
        backgroundColor: "#0078ff66",
      },
      {
        label: "Timeouts",
        data: podTimeouts,
        backgroundColor: "#ff6b6b66",
      },
    ],
  };

  // Chart 4 – Request Distribution
  const compData = {
    labels: Object.keys(errors_by_component),
    datasets: [
      {
        label: "Errors",
        data: Object.values(errors_by_component),
        backgroundColor: "#a5d8ff",
      },
    ],
  };

  return (
    <div className="viz-panel">
      <div className={`viz-card ${highlight.severity ? "highlight" : ""}`}>
        <h3>Severity Breakdown</h3>
        <Pie data={severityData} />
      </div>

      <div className={`viz-card ${highlight.timeline ? "highlight" : ""}`}>
        <h3>Error Timeline (hrs)</h3>
        <Line data={timelineData} />
      </div>

      <div className={`viz-card ${highlight.pods ? "highlight" : ""}`}>
        <h3>Pod Performance</h3>
        <Bar data={podData} />
      </div>

      <div className={`viz-card ${highlight.components ? "highlight" : ""}`}>
        <h3>Error Distribution by Component</h3>
        <Bar data={compData} />
      </div>
    </div>
  );
}
