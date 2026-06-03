import subprocess

def run(cmd):
    print(f"\n▶ Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise Exception(f"Failed: {cmd}")

def main():
    print("========== STARTING FULL PIPELINE ==========")

    # Core analytics
    run("python -m pipeline.analytics")

    # Dwell time
    run("python -m pipeline.dwell_time")
    run("python -m pipeline.dwell_analytics")

    # Journey analysis
    run("python -m pipeline.journeys")

    # Heatmap
    run("python -m pipeline.heatmap")

    # Sales analytics
    run("python -m pipeline.sales_analytics")

    # Anomaly detection
    run("python -m pipeline.anomaly_detection")

    # Funnel analysis
    run("python -m pipeline.funnel")

    print("========== PIPELINE COMPLETED ==========")

if __name__ == "__main__":
    main()