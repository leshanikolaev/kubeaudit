from kubeaudit.checks import check_latest_tag, check_missing_limits


def test_latest_tag_found():
    dep = {
        "kind": "Deployment",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {"name": "nginx", "image": "nginx:latest"},
                        {
                            "name": "istio-proxy",
                            "image": "docker.io/istio/proxyv2:1.24.0",
                        },
                    ]
                }
            }
        },
    }

    result = check_latest_tag(dep)

    assert len(result) == 1
    assert result[0].check_id == "image-latest-tag"


def test_latest_tag_not_found():
    dep = {
        "kind": "Deployment",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": "istio-proxy",
                            "image": "docker.io/istio/proxyv2:1.24.0",
                        },
                    ]
                }
            }
        },
    }

    result = check_latest_tag(dep)

    assert len(result) == 0


def test_empty_containers():
    dep = {
        "kind": "Deployment",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "template": {
                "spec": {"containers": []},
            }
        },
    }

    result = check_latest_tag(dep)

    assert len(result) == 0


def test_latest_tag_two_found():
    dep = {
        "kind": "Deployment",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {"name": "nginx", "image": "nginx:latest"},
                        {"name": "redis", "image": "redis:latest"},
                    ]
                }
            }
        },
    }

    result = check_latest_tag(dep)

    assert len(result) == 2
    assert result[0].check_id == "image-latest-tag"


def test_image_without_tag():
    dep = {
        "kind": "Deployment",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {"name": "nginx", "image": "nginx"},
                    ]
                }
            }
        },
    }

    result = check_latest_tag(dep)

    assert len(result) == 1


def test_registry_with_port_without_tag():

    dep = {
        "kind": "Deployment",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {"name": "nginx", "image": "registry.local:5000/nginx"},
                    ]
                }
            }
        },
    }

    result = check_latest_tag(dep)

    assert len(result) == 1


def test_resource_without_containers():

    cm = {
        "kind": "ConfigMap",
        "metadata": {"name": "app-config", "namespace": "default"},
        "data": {"color": "blue"},
    }
    result = check_latest_tag(cm)

    assert len(result) == 0


def test_pod_with_latest():

    pod = {
        "kind": "Pod",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "containers": [
                {"name": "nginx", "image": "nginx:latest"},
            ]
        },
    }
    result = check_latest_tag(pod)

    assert len(result) == 1
    assert result[0].check_id == "image-latest-tag"


def test_init_container_with_latest():

    dep = {
        "kind": "Deployment",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "template": {
                "spec": {
                    "initContainers": [
                        {"name": "init", "image": "busybox:latest"},
                    ],
                    "containers": [
                        {"name": "nginx", "image": "nginx:1.27"},
                    ],
                }
            }
        },
    }
    result = check_latest_tag(dep)

    assert len(result) == 1
    assert result[0].check_id == "image-latest-tag"


def test_missing_limits_found():

    dep = {
        "kind": "Deployment",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {"name": "nginx", "image": "nginx:1.27"},
                    ]
                }
            }
        },
    }

    result = check_missing_limits(dep)

    assert len(result) == 1
    assert result[0].check_id == "missing-limits"


def test_limits_present_not_found():

    dep = {
        "kind": "Deployment",
        "metadata": {"name": "nginx", "namespace": "default"},
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": "nginx",
                            "image": "nginx:1.27",
                            "resources": {"limits": {"memory": "256Mi", "cpu": "500m"}},
                        },
                    ]
                }
            }
        },
    }

    result = check_missing_limits(dep)

    assert len(result) == 0
