# Azure ML E2E Workshop (Updated to 2020)

## Target Audience
Anyone who wants a comprehensive end-to-end understanding of Azure Machine Learning (AzureML).

## Key Goals
1. Understand the core concepts of AzureML
1. Understand how to use AzureML in an end-to-end fashion
1. Serve as a reference for common scenarios

## Agenda

### Workspace Concepts: infra setup, ARM, workspace setup, computes, datastores, setup

1. [Set up your workspace and compute](1-workspace-concepts/1-setup-compute.md)
1. [Register a dataset](1-workspace-concepts/2-dataset.md)
1. [Run AutoML from the UI](1-workspace-concepts/3-automl.md) (optional)
1. [Designer interface](1-workspace-concepts/4-designer.md) (optional)
1. [Clone git repo to Compute Instance](1-workspace-concepts/5-clone-git-repo.md)


### Datasets, Model Training (AML, HyperDrive and AutoML), Model Inference

#### Notebooks to run and research:

AML training including HyperDrive:
- [Notebook for plain vanilla Scikit-Learn model training in AML local compute (AML VM)](2-training-inference/local-compute/binayclassification-employee-attrition-notebook.ipynb)
- [Notebook for Scikit-Learn model training in AML remote compute and HyperDrive](2-training-inference/2.1-aml-training-and-hyperdrive/remote-training/binayclassification-employee-attrition-aml-compute-notebook.ipynb)

Interpretability:
- [Notebook for Model Interpretability in AML on local compute](2-training-inference/2.2-aml-interpretability/1-simple-feature-transformations-explain-local.ipynb)
- [Notebook for Model Interpretability on AML Compute](2-training-inference/2.2-aml-interpretability/2-explain-model-on-amlcompute.ipynb)

Automated ML:
- [Notebook for AutoML local compute](2-training-inference/2.3-automl-training/local-compute/binayclassification-employee-attrition-autoaml-local-compute.ipynb)
- [Notebook for AutoML remote compute](2-training-inference/2.3-automl-training/remote-compute/binayclassification-employee-attrition-autoaml-remote-amlcompute.ipynb)

Pipelines & Batch Inference:
- [Use a model for batch inference](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/machine-learning-pipelines/parallel-run/tabular-dataset-inference-iris.ipynb)


### MLOps (model management, deployment, inference, automation)

#### Tutorials for MLOps
- [Deploy a model](./3-mlops/deploy-attrition-model.ipynb)
- [Automate training & deployment](./3-mlops/mlopsworkshop.md)
- [Create automation workflow with EventGrid](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-event-grid#sample-scenarios)

### Enterprise Readiness
- [Enteprise Security Overview](https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-enterprise-security)
- [Manage access via RBAC](https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-assign-roles)
- [Managing compute quotas](https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-manage-quotas)
- [VNET integration](https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-enable-virtual-network)
- [Azure Monitor](https://docs.microsoft.com/en-us/azure/machine-learning/service/monitor-azure-machine-learning)

