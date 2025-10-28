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
        const res = await fetch("http://127.0.0.1:6969/api/stats");
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

  // Chart 1 – Severity Breakdown
  const severityData = {
    labels: Object.keys(stats.severity_counts),
    datasets: [
      {
        data: Object.values(stats.severity_counts),
        backgroundColor: ["#cce5ff", "#ffeeba", "#f5c6cb", "#f8d7da"],
      },
    ],
  };

  // Chart 2 – Error Timeline
  const timelineData = {
    labels: stats.timeline.map((t) => t.timestamp.slice(11, 16)),
    datasets: [
      {
        label: "Errors",
        data: stats.timeline.map((t) => t.errors),
        fill: true,
        borderColor: "#0078ff",
        tension: 0.3,
      },
    ],
  };

  // Chart 3 – Pod Performance
  const podNames = Object.keys(stats.pod_performance);
  const podLatency = podNames.map(
    (p) => stats.pod_performance[p].latency_avg_ms
  );
  const podTimeouts = podNames.map((p) => stats.pod_performance[p].timeouts);

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
    labels: Object.keys(stats.errors_by_component),
    datasets: [
      {
        label: "Errors",
        data: Object.values(stats.errors_by_component),
        backgroundColor: "#a5d8ff",
      },
    ],
  };

  // Chart 5 – Security Events
  const secData = {
    labels: ["Auth Fails", "Network Timeouts"],
    datasets: [
      {
        data: [stats.auth_fails, stats.network_timeouts],
        backgroundColor: ["#ffb3b3", "#ffd6a5"],
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

      <div className={`viz-card ${highlight.security ? "highlight" : ""}`}>
        <h3>Auth / Network Anomalies</h3>
        <Pie data={secData} />
      </div>
    </div>
  );
}
