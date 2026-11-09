from kubeaudit.checks import check_latest_tag

def test_latest_tag_found():
    dep = {
    "kind": "Deployment",
    "metadata": {"name": "nginx", "namespace": "default"},
    "spec": {"template": {"spec": {"containers": [
        {"name": "nginx", "image": "nginx:latest"},
        {"name": "istio-proxy", "image": "docker.io/istio/proxyv2:1.24.0"},
    ]}}},
    }

    result = check_latest_tag(dep)

    assert len(result) == 1
    assert result[0].check_id == "image-latest-tag"

def test_latest_tag_no_found():
    dep = {
    "kind": "Deployment",
    "metadata": {"name": "nginx", "namespace": "default"},
    "spec": {"template": {"spec": {"containers": [
        {"name": "istio-proxy", "image": "docker.io/istio/proxyv2:1.24.0"},
    ]}}},
    }

    result = check_latest_tag(dep)

    assert len(result) == 0

def test_empty_containers():
    dep = {
    "kind": "Deployment",
    "metadata": {"name": "nginx", "namespace": "default"},
    "spec": {"template": {"spec": {"containers": []},
    }},
    }

    result = check_latest_tag(dep)

    assert len(result) == 0

def test_latest_tag_two_found():
    dep = {
    "kind": "Deployment",
    "metadata": {"name": "nginx", "namespace": "default"},
    "spec": {"template": {"spec": {"containers": [
        {"name": "nginx", "image": "nginx:latest"},
        {"name": "nginx", "image": "nginx:latest"},
    ]}}},
    }

    result = check_latest_tag(dep)

    assert len(result) == 2
    assert result[0].check_id == "image-latest-tag"