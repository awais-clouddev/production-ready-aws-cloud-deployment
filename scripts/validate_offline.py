"""Local repository checks only: no AWS SDK, AWS CLI or network calls."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "fde82881e3cb7b83c7568c1cf1a56c16caad9729"


def load(relative):
    return json.loads((ROOT / relative).read_text())


def main():
    files = list((ROOT / "reference").rglob("*.json"))
    for path in files:
        json.loads(path.read_text())
    print(f"PASS: {len(files)} reference JSON files parse")

    provenance = load("reference/application-provenance.json")
    assert re.fullmatch(r"[0-9a-f]{40}", provenance["reference_source_commit"])
    assert provenance["historically_deployed_source_commit"] is None
    assert provenance["historically_deployed_image_digests"] is None
    schema = ROOT / provenance["schema_reference_path"]
    assert hashlib.sha256(schema.read_bytes()).hexdigest() == provenance["schema_sha256"]
    print("PASS: source provenance and schema integrity")

    for name, port in (("frontend", 80), ("api", 8000)):
        task = load(f"reference/ecs/{name}-task-definition.template.json")
        service = load(f"reference/ecs/{name}-service.template.json")
        assert task["networkMode"] == "awsvpc"
        assert task["requiresCompatibilities"] == ["FARGATE"]
        assert (task["cpu"], task["memory"]) == ("256", "512")
        container = task["containerDefinitions"][0]
        assert container["name"] == name
        assert container["portMappings"][0]["containerPort"] == port
        assert "@sha256:<" in container["image"]
        assert "<ACCOUNT_ID>" in task["executionRoleArn"]
        assert service["desiredCount"] == 1
        network = service["networkConfiguration"]["awsvpcConfiguration"]
        assert network["assignPublicIp"] == "DISABLED"
        assert len(network["subnets"]) == 2
        target = service["loadBalancers"][0]
        assert target["containerName"] == container["name"]
        assert target["containerPort"] == port
        assert not any(
            item["name"] == "DATABASE_PASSWORD"
            for item in container.get("environment", [])
        )
    api = load("reference/ecs/api-task-definition.template.json")
    secret = api["containerDefinitions"][0]["secrets"][0]
    assert secret["name"] == "DATABASE_PASSWORD"
    policy = load("reference/iam/api-execution-policy.template.json")
    secret_statements = [
        s for s in policy["Statement"]
        if s["Action"] == "secretsmanager:GetSecretValue"
    ]
    assert len(secret_statements) == 1
    assert secret_statements[0]["Resource"] == secret["valueFrom"]
    print("PASS: reference task/service relationships and secret-policy scope")

    documents = [ROOT / "README.md"]
    documents += list((ROOT / "docs").glob("*.md"))
    documents += list((ROOT / "reference").glob("*.md"))
    fence = chr(96) * 3
    for path in documents:
        text = path.read_text()
        assert sum(line.startswith(fence) for line in text.splitlines()) % 2 == 0, path
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if re.match(r"(https?://|mailto:|#)", target):
                continue
            relative = target.split("#", 1)[0]
            assert (path.parent / relative).exists(), (path.name, target)
    print("PASS: Markdown fences and local document/image links")

    historical_pages = ["README.md"] + [
        f"docs/{name}.md" for name in (
            "architecture", "cost-management", "deployment", "networking",
            "observability", "security", "troubleshooting", "validation"
        )
    ]
    for relative in historical_pages:
        assert (ROOT / relative).read_text().count("**Deployment status:**") == 1
    print("PASS: historical deployment notices")

    tracked = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASELINE],
        cwd=ROOT, text=True
    ).splitlines()
    images = [name for name in tracked if name.endswith(".png")]
    for name in images:
        expected = subprocess.check_output(
            ["git", "rev-parse", f"{BASELINE}:{name}"],
            cwd=ROOT, text=True
        ).strip()
        actual = subprocess.check_output(
            ["git", "hash-object", "--", name],
            cwd=ROOT, text=True
        ).strip()
        assert actual == expected, f"Historical image changed: {name}"
    print(f"PASS: {len(images)} historical images unchanged")
    print("Offline checks passed. AWS API acceptance and runtime behavior are not verified.")


if __name__ == "__main__":
    main()
