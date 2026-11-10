from kubeaudit.models import Finding, Severity


def get_pod_spec(resource):
    if resource.get("kind") == "Pod":
        return resource.get("spec", {})
    return resource.get("spec", {}).get("template", {}).get("spec", {})


def get_containers(resource):
    pod_spec = get_pod_spec(resource)
    return pod_spec.get("containers", []) + pod_spec.get("initContainers", [])


def check_latest_tag(resource):
    result = []
    for container in get_containers(resource):
        last_part = container["image"].split("/")[-1]
        if container["image"].endswith(":latest") or ":" not in last_part:
            result.append(
                Finding(
                    check_id="image-latest-tag",
                    severity=Severity.WARNING,
                    kind=resource["kind"],
                    namespace=resource["metadata"]["namespace"],
                    name=resource["metadata"]["name"],
                    message=f"container {container['name']} uses image {container['image']}",
                )
            )
    return result


def check_missing_limits(resource):
    result = []
    for container in get_containers(resource):
        if not container.get("resources", {}).get("limits", {}):
            result.append(
                Finding(
                    check_id="missing-limits",
                    severity=Severity.WARNING,
                    kind=resource["kind"],
                    namespace=resource["metadata"]["namespace"],
                    name=resource["metadata"]["name"],
                    message=f"container {container['name']} has no resource limits",
                )
            )
    return result


def check_missing_readiness_probe(resource):
    result = []
    for container in get_pod_spec(resource).get("containers", []):
        if not container.get("readinessProbe"):
            result.append(
                Finding(
                    check_id="missing-readiness-probe",
                    severity=Severity.WARNING,
                    kind=resource["kind"],
                    namespace=resource["metadata"]["namespace"],
                    name=resource["metadata"]["name"],
                    message=f"container {container['name']} has no readiness probe",
                )
            )
    return result
