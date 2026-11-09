from kubeaudit.models import Finding, Severity


def check_latest_tag(resource):
    result = []
    if resource.get("kind") == "Pod":
        pod_spec = resource.get("spec", {})
    else:
        pod_spec = resource.get("spec", {}).get("template", {}).get("spec", {})
    for container in pod_spec.get("containers", []) + pod_spec.get(
        "initContainers", []
    ):
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
