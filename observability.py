import logging
import boto3

logger = logging.getLogger("rag_agent")
logger.setLevel(logging.INFO)


def record_metric(name: str, value: float) -> None:
    """Publish a custom CloudWatch metric."""
    try:
        cw = boto3.client("cloudwatch")
        cw.put_metric_data(
            Namespace="RAGAgent",
            MetricData=[{"MetricName": name, "Value": value}],
        )
    except Exception as exc:
        logger.error("Failed to record metric %s: %s", name, exc)
