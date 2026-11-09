from kubeaudit.models import Finding, Severity

def check_latest_tag(resource):
    result = []
    for container in resource["spec"]["template"]["spec"]["containers"]:
        if container["image"].endswith(":latest") or ":" not in container["image"]:
            result.append(
                Finding(
                    check_id="image-latest-tag",
                    severity=Severity.WARNING,
                    kind=resource["kind"],
                    namespace=resource["metadata"]["namespace"],
                    name=resource["metadata"]["name"],
                    message=f"container {container['name']} uses image {container['image']}"
                )
            )
    return result