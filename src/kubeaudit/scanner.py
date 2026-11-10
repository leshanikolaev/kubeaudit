from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

from kubeaudit.checks import (
    check_latest_tag,
    check_missing_limits,
    check_missing_readiness_probe,
)


def audit_namespace(namespace):
    config.load_kube_config()

    try:
        client.CoreV1Api().read_namespace(namespace)
    except ApiException as e:
        if e.status == 404:
            raise ValueError(f"namespace {namespace} not found")
        raise

    apps = client.AppsV1Api()
    deps = apps.list_namespaced_deployment(namespace)
    api = client.ApiClient()

    result = []
    for item in deps.items:
        d = api.sanitize_for_serialization(item)
        d["kind"] = "Deployment"
        result += check_latest_tag(d)
        result += check_missing_limits(d)
        result += check_missing_readiness_probe(d)
    return result


if __name__ == "__main__":
    try:
        for finding in audit_namespace("default"):
            print(finding.severity.value, finding.kind, finding.name, finding.message)
    except ValueError as e:
        print(e)
