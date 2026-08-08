#!/usr/bin/env python3
"""Audit rendered Kubernetes objects without printing Secret values or contacting a cluster."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml_common as common

CLUSTER_SCOPED_KINDS = {
    "APIService", "CSIDriver", "CSINode", "ClusterRole", "ClusterRoleBinding",
    "CustomResourceDefinition", "IngressClass", "MutatingWebhookConfiguration",
    "Namespace", "Node", "PersistentVolume", "PodSecurityPolicy", "PriorityClass",
    "RuntimeClass", "StorageClass", "ValidatingAdmissionPolicy",
    "ValidatingAdmissionPolicyBinding", "ValidatingWebhookConfiguration", "VolumeAttachment",
}
WORKLOAD_KINDS = {"Deployment", "StatefulSet", "DaemonSet", "ReplicaSet", "ReplicationController"}
ALLOWED_RESTRICTED_VOLUME_TYPES = {
    "configMap", "csi", "downwardAPI", "emptyDir", "ephemeral", "persistentVolumeClaim",
    "projected", "secret",
}
DNS_LABEL = re.compile(r"^[a-z0-9](?:[-a-z0-9]*[a-z0-9])?$")


@dataclass(frozen=True)
class ObjectId:
    api_version: str
    kind: str
    namespace: str
    name: str

    def display(self) -> str:
        return f"{self.api_version}/{self.kind} {self.namespace or '<cluster>'}/{self.name}"


@dataclass(frozen=True)
class Reference:
    resource: str
    namespace: str
    ref_kind: str
    name: str
    key: str
    field: str
    optional: bool


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    resource: str
    field: str
    message: str
    category: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--default-namespace", default="default")
    parser.add_argument("--allow-external-ref", action="append", default=[],
                        help="Kind/name or Kind/namespace/name; repeat explicitly")
    parser.add_argument("--pod-security-profile", choices=("none", "baseline", "restricted"), default="baseline")
    parser.add_argument("--warnings-as-errors", action="store_true")
    parser.add_argument("--max-bytes", type=int, default=16 * 1024 * 1024)
    parser.add_argument("--max-documents", type=int, default=10_000)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def object_id(resource: Mapping[str, Any], default_namespace: str) -> ObjectId:
    metadata = resource.get("metadata") if isinstance(resource.get("metadata"), Mapping) else {}
    kind = str(resource.get("kind") or "")
    namespace = "" if kind in CLUSTER_SCOPED_KINDS else str(metadata.get("namespace") or default_namespace)
    return ObjectId(
        str(resource.get("apiVersion") or ""),
        kind,
        namespace,
        str(metadata.get("name") or ""),
    )


def pod_spec(resource: Mapping[str, Any]) -> Mapping[str, Any] | None:
    kind = resource.get("kind")
    spec = resource.get("spec") if isinstance(resource.get("spec"), Mapping) else {}
    if kind == "Pod":
        return spec
    if kind in WORKLOAD_KINDS | {"Job"}:
        template = spec.get("template") if isinstance(spec.get("template"), Mapping) else {}
        return template.get("spec") if isinstance(template.get("spec"), Mapping) else {}
    if kind == "CronJob":
        job_template = spec.get("jobTemplate") if isinstance(spec.get("jobTemplate"), Mapping) else {}
        job_spec = job_template.get("spec") if isinstance(job_template.get("spec"), Mapping) else {}
        template = job_spec.get("template") if isinstance(job_spec.get("template"), Mapping) else {}
        return template.get("spec") if isinstance(template.get("spec"), Mapping) else {}
    return None


def containers(spec: Mapping[str, Any]) -> Iterable[tuple[str, Mapping[str, Any]]]:
    for field in ("initContainers", "containers", "ephemeralContainers"):
        values = spec.get(field) if isinstance(spec.get(field), Sequence) else []
        for index, container in enumerate(values):
            if isinstance(container, Mapping):
                yield f"{field}[{index}]", container


def append_reference(
    refs: list[Reference], oid: ObjectId, kind: str, name: Any, field: str,
    *, key: Any = "", optional: Any = False, namespace: str | None = None,
) -> None:
    if name:
        refs.append(
            Reference(oid.display(), namespace if namespace is not None else oid.namespace, kind,
                      str(name), str(key or ""), field, bool(optional))
        )


def collect_references(resource: Mapping[str, Any], oid: ObjectId) -> list[Reference]:
    refs: list[Reference] = []
    spec = pod_spec(resource)
    if spec is not None:
        for index, item in enumerate(spec.get("imagePullSecrets") or []):
            if isinstance(item, Mapping):
                append_reference(refs, oid, "Secret", item.get("name"), f"spec.imagePullSecrets[{index}].name")
        append_reference(refs, oid, "ServiceAccount", spec.get("serviceAccountName"), "spec.serviceAccountName")

        volume_names: set[str] = set()
        for index, volume in enumerate(spec.get("volumes") or []):
            if not isinstance(volume, Mapping):
                continue
            if volume.get("name"):
                volume_names.add(str(volume["name"]))
            secret = volume.get("secret") if isinstance(volume.get("secret"), Mapping) else {}
            append_reference(refs, oid, "Secret", secret.get("secretName"),
                             f"spec.volumes[{index}].secret.secretName", optional=secret.get("optional"))
            config_map = volume.get("configMap") if isinstance(volume.get("configMap"), Mapping) else {}
            append_reference(refs, oid, "ConfigMap", config_map.get("name"),
                             f"spec.volumes[{index}].configMap.name", optional=config_map.get("optional"))
            pvc = volume.get("persistentVolumeClaim") if isinstance(volume.get("persistentVolumeClaim"), Mapping) else {}
            append_reference(refs, oid, "PersistentVolumeClaim", pvc.get("claimName"),
                             f"spec.volumes[{index}].persistentVolumeClaim.claimName")
            projected = volume.get("projected") if isinstance(volume.get("projected"), Mapping) else {}
            for source_index, source in enumerate(projected.get("sources") or []):
                if not isinstance(source, Mapping):
                    continue
                secret_source = source.get("secret") if isinstance(source.get("secret"), Mapping) else {}
                append_reference(refs, oid, "Secret", secret_source.get("name"),
                                 f"spec.volumes[{index}].projected.sources[{source_index}].secret.name",
                                 optional=secret_source.get("optional"))
                cm_source = source.get("configMap") if isinstance(source.get("configMap"), Mapping) else {}
                append_reference(refs, oid, "ConfigMap", cm_source.get("name"),
                                 f"spec.volumes[{index}].projected.sources[{source_index}].configMap.name",
                                 optional=cm_source.get("optional"))

        for container_field, container in containers(spec):
            for index, env_from in enumerate(container.get("envFrom") or []):
                if not isinstance(env_from, Mapping):
                    continue
                secret_ref = env_from.get("secretRef") if isinstance(env_from.get("secretRef"), Mapping) else {}
                append_reference(refs, oid, "Secret", secret_ref.get("name"),
                                 f"spec.{container_field}.envFrom[{index}].secretRef.name",
                                 optional=secret_ref.get("optional"))
                cm_ref = env_from.get("configMapRef") if isinstance(env_from.get("configMapRef"), Mapping) else {}
                append_reference(refs, oid, "ConfigMap", cm_ref.get("name"),
                                 f"spec.{container_field}.envFrom[{index}].configMapRef.name",
                                 optional=cm_ref.get("optional"))
            for index, env in enumerate(container.get("env") or []):
                if not isinstance(env, Mapping):
                    continue
                value_from = env.get("valueFrom") if isinstance(env.get("valueFrom"), Mapping) else {}
                secret_key = value_from.get("secretKeyRef") if isinstance(value_from.get("secretKeyRef"), Mapping) else {}
                append_reference(refs, oid, "Secret", secret_key.get("name"),
                                 f"spec.{container_field}.env[{index}].valueFrom.secretKeyRef",
                                 key=secret_key.get("key"), optional=secret_key.get("optional"))
                cm_key = value_from.get("configMapKeyRef") if isinstance(value_from.get("configMapKeyRef"), Mapping) else {}
                append_reference(refs, oid, "ConfigMap", cm_key.get("name"),
                                 f"spec.{container_field}.env[{index}].valueFrom.configMapKeyRef",
                                 key=cm_key.get("key"), optional=cm_key.get("optional"))
            for index, mount in enumerate(container.get("volumeMounts") or []):
                if isinstance(mount, Mapping):
                    name = str(mount.get("name") or "")
                    if name and name not in volume_names:
                        refs.append(Reference(oid.display(), oid.namespace, "Volume", name, "",
                                              f"spec.{container_field}.volumeMounts[{index}].name", False))

    kind = resource.get("kind")
    raw_spec = resource.get("spec") if isinstance(resource.get("spec"), Mapping) else {}
    if kind == "Ingress":
        for index, tls in enumerate(raw_spec.get("tls") or []):
            if isinstance(tls, Mapping):
                append_reference(refs, oid, "Secret", tls.get("secretName"), f"spec.tls[{index}].secretName")
        rules = raw_spec.get("rules") or []
        for rule_index, rule in enumerate(rules):
            if not isinstance(rule, Mapping):
                continue
            http = rule.get("http") if isinstance(rule.get("http"), Mapping) else {}
            for path_index, path_item in enumerate(http.get("paths") or []):
                if not isinstance(path_item, Mapping):
                    continue
                backend = path_item.get("backend") if isinstance(path_item.get("backend"), Mapping) else {}
                service = backend.get("service") if isinstance(backend.get("service"), Mapping) else {}
                append_reference(refs, oid, "Service", service.get("name"),
                                 f"spec.rules[{rule_index}].http.paths[{path_index}].backend.service.name")
    if kind == "ServiceAccount":
        for field in ("secrets", "imagePullSecrets"):
            for index, item in enumerate(resource.get(field) or []):
                if isinstance(item, Mapping):
                    append_reference(refs, oid, "Secret", item.get("name"), f"{field}[{index}].name")
    if kind in {"RoleBinding", "ClusterRoleBinding"}:
        role_ref = resource.get("roleRef") if isinstance(resource.get("roleRef"), Mapping) else {}
        role_kind = str(role_ref.get("kind") or "")
        role_namespace = "" if role_kind == "ClusterRole" else oid.namespace
        append_reference(refs, oid, role_kind, role_ref.get("name"), "roleRef.name", namespace=role_namespace)
        for index, subject in enumerate(resource.get("subjects") or []):
            if isinstance(subject, Mapping) and subject.get("kind") == "ServiceAccount":
                append_reference(refs, oid, "ServiceAccount", subject.get("name"),
                                 f"subjects[{index}].name",
                                 namespace=str(subject.get("namespace") or oid.namespace))
    if kind in {"HorizontalPodAutoscaler", "PodDisruptionBudget"}:
        target = raw_spec.get("scaleTargetRef") if isinstance(raw_spec.get("scaleTargetRef"), Mapping) else {}
        if target:
            append_reference(refs, oid, str(target.get("kind") or ""), target.get("name"),
                             "spec.scaleTargetRef.name")
    return refs


def data_keys(resource: Mapping[str, Any]) -> set[str]:
    if resource.get("kind") not in {"Secret", "ConfigMap"}:
        return set()
    keys: set[str] = set()
    for field in ("data", "stringData", "binaryData"):
        value = resource.get(field)
        if isinstance(value, Mapping):
            keys.update(str(key) for key in value)
    return keys


def parse_allowed(values: list[str]) -> set[tuple[str, str, str]]:
    allowed: set[tuple[str, str, str]] = set()
    for value in values:
        parts = value.split("/")
        if len(parts) == 2:
            kind, name = parts
            namespace = "*"
        elif len(parts) == 3:
            kind, namespace, name = parts
        else:
            raise common.InputError(
                f"invalid --allow-external-ref {value!r}; use Kind/name or Kind/namespace/name"
            )
        if not all(parts):
            raise common.InputError(f"empty component in --allow-external-ref {value!r}")
        allowed.add((kind, namespace, name))
    return allowed


def allowed_reference(reference: Reference, allowed: set[tuple[str, str, str]]) -> bool:
    return (
        (reference.ref_kind, reference.namespace, reference.name) in allowed
        or (reference.ref_kind, "*", reference.name) in allowed
    )


def security_findings(resource: Mapping[str, Any], oid: ObjectId, profile: str) -> list[Finding]:
    if profile == "none":
        return []
    spec = pod_spec(resource)
    if spec is None:
        return []
    findings: list[Finding] = []

    def add(severity: str, code: str, field: str, message: str) -> None:
        findings.append(Finding(severity, code, oid.display(), field, message, "pod-security"))

    for field in ("hostNetwork", "hostPID", "hostIPC"):
        if spec.get(field) is True:
            add("error", f"pod-security-{field.lower()}", f"spec.{field}", f"{field} is forbidden by the selected Pod Security profile")
    pod_security = spec.get("securityContext") if isinstance(spec.get("securityContext"), Mapping) else {}
    if profile == "restricted":
        if pod_security.get("runAsNonRoot") is not True:
            add("warning", "pod-security-run-as-non-root", "spec.securityContext.runAsNonRoot",
                "restricted profile expects runAsNonRoot: true at pod or container scope")
        seccomp = pod_security.get("seccompProfile") if isinstance(pod_security.get("seccompProfile"), Mapping) else {}
        if seccomp.get("type") not in {"RuntimeDefault", "Localhost"}:
            add("warning", "pod-security-seccomp", "spec.securityContext.seccompProfile.type",
                "restricted profile expects RuntimeDefault or Localhost")

    for index, volume in enumerate(spec.get("volumes") or []):
        if not isinstance(volume, Mapping):
            continue
        if "hostPath" in volume:
            add("error", "pod-security-hostpath", f"spec.volumes[{index}].hostPath",
                "hostPath volumes are outside Baseline and Restricted profiles")
        if profile == "restricted":
            volume_types = {str(key) for key in volume if key != "name"}
            unsupported = volume_types - ALLOWED_RESTRICTED_VOLUME_TYPES
            if unsupported:
                add("error", "pod-security-volume-type", f"spec.volumes[{index}]",
                    f"restricted profile does not allow volume type(s): {', '.join(sorted(unsupported))}")

    for container_field, container in containers(spec):
        security = container.get("securityContext") if isinstance(container.get("securityContext"), Mapping) else {}
        if security.get("privileged") is True:
            add("error", "pod-security-privileged", f"spec.{container_field}.securityContext.privileged",
                "privileged containers are forbidden")
        ports = container.get("ports") if isinstance(container.get("ports"), Sequence) else []
        for index, port in enumerate(ports):
            if isinstance(port, Mapping) and int(port.get("hostPort") or 0) != 0:
                add("error", "pod-security-host-port", f"spec.{container_field}.ports[{index}].hostPort",
                    "hostPort is outside the selected baseline policy")
        if profile == "restricted":
            if security.get("allowPrivilegeEscalation") is not False:
                add("error", "pod-security-privilege-escalation",
                    f"spec.{container_field}.securityContext.allowPrivilegeEscalation",
                    "restricted profile requires allowPrivilegeEscalation: false")
            if security.get("runAsUser") == 0:
                add("error", "pod-security-root-user", f"spec.{container_field}.securityContext.runAsUser",
                    "restricted profile forbids runAsUser: 0")
            capabilities = security.get("capabilities") if isinstance(security.get("capabilities"), Mapping) else {}
            dropped = {str(value) for value in capabilities.get("drop") or []}
            added = {str(value) for value in capabilities.get("add") or []}
            if "ALL" not in dropped:
                add("error", "pod-security-capabilities-drop",
                    f"spec.{container_field}.securityContext.capabilities.drop",
                    "restricted profile requires dropping ALL capabilities")
            if added - {"NET_BIND_SERVICE"}:
                add("error", "pod-security-capabilities-add",
                    f"spec.{container_field}.securityContext.capabilities.add",
                    "restricted profile permits adding only NET_BIND_SERVICE")
            container_seccomp = security.get("seccompProfile") if isinstance(security.get("seccompProfile"), Mapping) else {}
            if not container_seccomp and pod_security.get("seccompProfile") is None:
                add("warning", "pod-security-container-seccomp",
                    f"spec.{container_field}.securityContext.seccompProfile",
                    "restricted profile expects a pod- or container-level seccomp profile")
    return findings


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    findings: list[Finding] = []
    objects: dict[tuple[str, str, str], tuple[ObjectId, Mapping[str, Any]]] = {}
    references: list[Reference] = []
    document_count = 0
    try:
        resolved, _, documents = common.load_documents(
            args.input, max_bytes=args.max_bytes, max_documents=args.max_documents
        )
        allowed = parse_allowed(args.allow_external_ref)
        for index, resource in enumerate(documents):
            if resource is None:
                continue
            document_count += 1
            if not isinstance(resource, Mapping):
                findings.append(Finding("error", "non-object-document", f"document[{index}]", "$",
                                        "rendered document root is not a mapping", "structure"))
                continue
            oid = object_id(resource, args.default_namespace)
            metadata = resource.get("metadata") if isinstance(resource.get("metadata"), Mapping) else {}
            if not oid.api_version or not oid.kind or not oid.name:
                generated = str(metadata.get("generateName") or "")
                detail = "metadata.generateName is not deterministic in rendered evidence" if generated else "object lacks apiVersion, kind, or metadata.name"
                findings.append(Finding("error", "incomplete-identity", oid.display(), "metadata", detail, "identity"))
                continue
            if oid.namespace and (len(oid.namespace) > 63 or not DNS_LABEL.fullmatch(oid.namespace)):
                findings.append(Finding("error", "invalid-namespace", oid.display(), "metadata.namespace",
                                        "namespace is not a DNS label", "identity"))
            identity = (oid.kind, oid.namespace, oid.name)
            if identity in objects:
                findings.append(Finding("error", "duplicate-object", oid.display(), "metadata",
                                        "duplicate kind/namespace/name identity", "identity"))
            else:
                objects[identity] = (oid, resource)
            findings.extend(security_findings(resource, oid, args.pod_security_profile))

        for oid, resource in objects.values():
            references.extend(collect_references(resource, oid))
        for reference in references:
            if reference.ref_kind == "Volume":
                findings.append(Finding("error", "dangling-volume-mount", reference.resource,
                                        reference.field, f"undefined volume {reference.name!r}", "reference"))
                continue
            target = objects.get((reference.ref_kind, reference.namespace, reference.name))
            if target is None:
                if reference.optional:
                    findings.append(Finding("warning", "optional-external-reference", reference.resource,
                                            reference.field, f"optional {reference.ref_kind} {reference.name!r} is not rendered", "reference"))
                elif allowed_reference(reference, allowed):
                    findings.append(Finding("warning", "allowed-external-reference", reference.resource,
                                            reference.field, f"documented external {reference.ref_kind} {reference.name!r} is not rendered", "reference"))
                else:
                    findings.append(Finding("error", "dangling-reference", reference.resource,
                                            reference.field, f"{reference.ref_kind} {reference.name!r} is not rendered in namespace {reference.namespace!r}", "reference"))
                continue
            if reference.key and reference.key not in data_keys(target[1]):
                findings.append(Finding("error", "missing-referenced-key", reference.resource,
                                        reference.field, f"{reference.ref_kind} {reference.name!r} does not render key {reference.key!r}", "reference"))
    except (OSError, common.InputError, ValueError) as exc:
        resolved = args.input
        findings.append(Finding("error", "analysis-failure", str(args.input), "$", str(exc), "tool"))

    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    coverage = [
        "offline object and reference checks do not replace Kubernetes OpenAPI or admission validation",
        "custom-resource scope and CRD-specific references are not inferred",
        "Pod Security checks are a bounded subset; use version-pinned policy tooling for full enforcement",
    ]
    if args.allow_external_ref:
        coverage.append("external references were accepted by explicit command-line allowlist")
    status = "failed" if errors or (args.warnings_as_errors and warnings) else ("incomplete" if warnings else "complete")
    result = {
        "status": status,
        "input": str(resolved),
        "document_count": document_count,
        "object_count": len(objects),
        "reference_count": len(references),
        "pod_security_profile": args.pod_security_profile,
        "errors": errors,
        "warnings": warnings,
        "coverage_gaps": coverage,
        "secret_values_emitted": False,
        "findings": [asdict(item) for item in findings],
    }

    if args.format == "json":
        print(common.stable_json(result), end="")
    else:
        for item in findings:
            print(f"{item.severity.upper():7} {item.code}: {item.resource} [{item.field}]: {item.message}")
        for gap in coverage:
            print(f"COVERAGE {gap}")
        print(f"Parsed {len(objects)} object(s), {len(references)} reference(s): {errors} error(s), {warnings} warning(s).")
    if status == "failed":
        return 1
    return 2 if status == "incomplete" else 0


if __name__ == "__main__":
    sys.exit(main())
