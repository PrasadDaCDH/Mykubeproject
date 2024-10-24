
In EKS everything related to Control plane is taken care by AWS
They will be highly available.
https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html

Farget:
It takes care of Data plane activities of Containers.
Its a aws serverless compute.

Prequisites for EKS:
https://docs.aws.amazon.com/eks/latest/userguide/setting-up.html
1> need to install Kubectl on the laptop
kubectl – A command line tool for working with Kubernetes clusters. For more information, see Installing or updating kubectl.

2>eksctl – A command line tool for working with EKS clusters that automates many individual tasks. For more information, see Installing or updating.

AWS CLI – A command line tool for working with AWS services, including Amazon EKS. For more information, see Installing, updating, and uninstalling the AWS CLI in the AWS Command Line Interface User Guide. After installing the AWS CLI, we recommend that you also configure it. For more information, see Quick configuration with aws configure in the AWS Command Line Interface User Guide.


1> Installing AWS cli on laptop
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
#curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#unzip awscliv2.zip
#sudo ./aws/install

2>Installing EKSCTL:
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz

sudo mv /tmp/eksctl /usr/local/bin

3>Installing Kubectl
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

**To deploy the CLuster**
eksctl create cluster --name demo-cluster --region ap-south-1 --fargate

**Configuring kubectl for EKS:**

Once kubectl is installed, you need to configure it to work with your EKS cluster.
In the AWS Management Console, go to the EKS service and select your cluster.
Click on the "Config" button and follow the instructions to update your kubeconfig file. Alternatively, you can use the AWS CLI to update the kubeconfig file:

aws eks update-kubeconfig --name demo-cluster --region ap-south-1

Verify the configuration by running a kubectl command against your EKS cluster:

kubectl get nodes -n kube-system

**deployment of the Application**

**Create Fargate profile**
eksctl create fargateprofile \
    --cluster demo-cluster \
    --region ap-south-1 \
    --name alb-sample-app \
    --namespace game-2048

**Deploying the app**

kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/examples/2048/2048_full.yaml

**commands to configure IAM OIDC provider**
If you want the pods to get access to aws resource we need to configure IAM OIDC provoider access

export cluster_name=demo-cluster
oidc_id=$(aws eks describe-cluster --name demo-cluster --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5) 

**TO associate the oidc with IAM**
eksctl utils associate-iam-oidc-provider --cluster demo-cluster --approve

**Now to setup the ALB for the controller**
How to setup alb add on
Download IAM policy

curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/install/iam_policy.json

Create IAM Policy

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json


Create IAM Role

eksctl create iamserviceaccount \
  --cluster=demo-cluster \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::<your-aws-account-id>:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve

**Deploy ALB controller**

Add helm repo

helm repo add eks https://aws.github.io/eks-charts

**Update the repo**

helm repo update eks

**To install the Load balancer for the pod**

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \            
  -n kube-system \
  --set clusterName=<your-cluster-name> \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=<region> \
  --set vpcId=<your-vpc-id>

**Verify that the deployments are running**

kubectl get deployment -n kube-system aws-load-balancer-controller

  



