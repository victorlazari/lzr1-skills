# Advanced DevOps Specialist: Complete Reference Guide

## Table of Contents
1. [Introduction](#1-introduction)
2. [Amazon Web Services (AWS) for DevOps](#2-amazon-web-services-aws-for-devops)
3. [Kubernetes: Architecture and Advanced Concepts](#3-kubernetes-architecture-and-advanced-concepts)
4. [Amazon Elastic Kubernetes Service (EKS)](#4-amazon-elastic-kubernetes-service-eks)
5. [Helm and Kustomize](#5-helm-and-kustomize)
6. [GitOps and Modern CI/CD](#6-gitops-and-modern-cicd)
7. [Virtual Private Cloud (VPC) and Networking](#7-virtual-private-cloud-vpc-and-networking)
8. [Configuration Schemas Guide](#8-configuration-schemas-guide)

---

## 1. Introduction
The role of a DevOps Specialist bridges development and operations to foster continuous integration, continuous delivery, and seamless infrastructure management using modern 2026 practices.

## 2. Amazon Web Services (AWS) for DevOps
AWS provides a robust cloud platform. Key services include EC2, EKS, S3, CloudFormation, and VPC.
- **IaC:** Use Terraform or CloudFormation for reproducible infrastructure.
- **Security:** Implement fine-grained IAM roles with least privilege.

## 3. Kubernetes: Architecture and Advanced Concepts
- **Control Plane & Nodes:** Understand API Server, etcd, Scheduler, and kubelet.
- **Networking:** Pod-to-pod communication via CNI plugins (e.g., AWS VPC CNI).
- **Storage:** Manage stateful workloads with PVs and PVCs.

## 4. Amazon Elastic Kubernetes Service (EKS)
- **Best Practices:** Deploy worker nodes in private subnets, use managed node groups, and implement cluster autoscaling.
- **IAM Integration:** Leverage IAM Roles for Service Accounts (IRSA).

## 5. Helm and Kustomize
- **Helm:** Manages Kubernetes applications through charts for templating and versioning.
- **Kustomize:** Native Kubernetes configuration management.
- **Combined Usage:** Use Helm for packaging and distribution, and Kustomize for environment-specific patching and overlays. This provides the best of both worlds: reusable charts and declarative, template-free customization.

## 6. GitOps and Modern CI/CD
- **Trunk-Based Development:** Short-lived branches with frequent merges to trunk. Avoid outdated branching strategies like Git Flow.
- **Directory-Based Environment Separation:** Separate environments (dev, staging, prod) using directory structures rather than branches to prevent drift and simplify access control.
- **Separation of Concerns:** Keep application code and deployment configuration in separate repositories to trigger deployments independently of code builds.
- **Pull-Based Deployments:** Use GitOps controllers (Argo CD, Flux) that pull changes from Git, rather than CI pipelines pushing to clusters.
- **Webhook Receivers:** Configure webhook receivers for GitOps controllers to trigger immediate synchronization upon Git commits, avoiding API rate limits associated with polling.
- **Ephemeral Testing Environments:** Spin up isolated, on-demand environments for testing pull requests, tearing them down after merge to save costs and ensure clean test states.

## 7. Virtual Private Cloud (VPC) and Networking
- **Design:** Use Public/Private Subnets, NAT Gateways, and Security Groups.
- **EKS Networking:** Pods receive IPs from VPC CIDR blocks via AWS VPC CNI.

## 8. Configuration Schemas Guide
- **Terraform:** HCL (`main.tf`, `variables.tf`).
- **GitHub Actions:** YAML in `.github/workflows/`.
- **Kubernetes:** YAML manifests (`apiVersion`, `kind`, `metadata`, `spec`).
