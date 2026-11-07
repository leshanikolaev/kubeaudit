def check_latest_tag(resource):
    result = []
    for container in resource["spec"]["template"]["spec"]["containers"]:
        if container["image"].endswith(":latest"):
            result.append(container["image"])
    return result