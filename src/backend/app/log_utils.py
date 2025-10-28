import os
import json
from collections import defaultdict
import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "../../../data/logs")

def parse_log_file(file_path):
    """Parses a single JSONL log file and returns a list of log entries."""
    logs = []
    with open(file_path, "r") as f:
        for line in f:
            try:
                logs.append(json.loads(line))
            except json.JSONDecodeError:
                # Ignore lines that are not valid JSON
                pass
    return logs

def get_aggregated_log_stats():
    """
    Reads all log files, aggregates the data, and returns a dictionary
    with the statistics required by the frontend.
    """
    all_logs = []
    for filename in os.listdir(LOG_DIR):
        if filename.endswith(".jsonl.log"):
            file_path = os.path.join(LOG_DIR, filename)
            all_logs.extend(parse_log_file(file_path))

    severity_counts = defaultdict(int)
    errors_by_component = defaultdict(int)
    timeline = defaultdict(lambda: defaultdict(int))
    pod_performance = defaultdict(lambda: {'latencies': [], 'timeouts': 0})
    auth_fails = 0
    network_timeouts = 0

    for log in all_logs:
        severity = log.get("level", "UNKNOWN").upper()
        severity_counts[severity] += 1

        component = log.get("pod", "unknown").split("-")[0]
        if severity == "ERROR":
            errors_by_component[component] += 1

        timestamp_str = log.get("ts")
        if timestamp_str:
            dt = datetime.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            hour_str = dt.strftime("%Y-%m-%dT%H:00:00Z")
            if severity == "ERROR":
                timeline[hour_str]['errors'] += 1

        pod_name = log.get("pod")
        if pod_name:
            latency = log.get("lat_ms")
            if latency is not None:
                pod_performance[pod_name]['latencies'].append(latency)
            if log.get("event") == "timeout":
                pod_performance[pod_name]['timeouts'] += 1
        
        if "auth" in log.get("event", "") and severity == "ERROR":
            auth_fails += 1
        
        if "network" in log.get("event", "") and severity == "ERROR":
            network_timeouts += 1


    # Process aggregated data for the final response format
    processed_timeline = sorted(
        [{"timestamp": ts, "errors": data["errors"]} for ts, data in timeline.items()],
        key=lambda x: x["timestamp"],
    )

    processed_pod_performance = {
        pod: {
            "latency_avg_ms": sum(data['latencies']) / len(data['latencies']) if data['latencies'] else 0,
            "timeouts": data['timeouts'],
        }
        for pod, data in pod_performance.items()
    }

    return {
        "severity_counts": dict(severity_counts),
        "errors_by_component": dict(errors_by_component),
        "timeline": processed_timeline,
        "pod_performance": processed_pod_performance,
        "auth_fails": auth_fails,
        "network_timeouts": network_timeouts,
    }
