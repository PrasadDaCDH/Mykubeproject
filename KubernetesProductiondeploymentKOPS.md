How to Crete Kubernetes production grade cluster on ec2_instance ubuntu using kops?

We on the production manage kubernetes operations using kops only

What is KOPS in kubernetes?
Kops (Kubernetes Operations) is a tool that simplifies the deployment, management, and maintenance of Kubernetes clusters on cloud providers, primarily on AWS. It’s one of the most popular tools for managing production-grade Kubernetes clusters, offering a higher level of automation and ease of use.


Create the cluster by following below:

Creating a Kubernetes 3-node cluster using Kops on AWS with EC2 instances running Ubuntu involves several steps. Below is a detailed guide to help you set up your cluster.

### **Prerequisites**

1. **AWS Account**: Ensure you have an AWS account with the necessary permissions to create resources.
2. **AWS CLI**: Install and configure the AWS CLI on your local machine.
3. **Kops**: Install Kops on your local machine.
4. **kubectl**: Install `kubectl` on your local machine to interact with your Kubernetes cluster.
5. **S3 Bucket**: You'll need an S3 bucket to store the Kops state.

### **Step 1: Install and Configure AWS CLI**

If you haven't already, install the AWS CLI and configure it with your credentials:

```bash
sudo apt-get update
sudo apt-get install awscli -y
aws configure
```

### **Step 2: Install Kops**

Install Kops on your local machine:

```bash
curl -Lo kops https://github.com/kubernetes/kops/releases/latest/download/kops-linux-amd64
chmod +x ./kops
sudo mv ./kops /usr/local/bin/
```

### **Step 3: Install kubectl**

Install `kubectl` to manage the Kubernetes cluster:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/
```

### **Step 4: Create an S3 Bucket for Kops State**

Kops uses an S3 bucket to store the cluster state:

```bash
aws s3api create-bucket --bucket <your-kops-state-store> --region us-east-1
```

Set the S3 bucket as your Kops state store environment variable:

```bash
export KOPS_STATE_STORE=s3://<your-kops-state-store>
```

### **Step 5: Create a DNS Domain for Your Cluster**

Kops requires a DNS domain to manage your cluster. You can use Route 53 or an existing domain:

1. **Create a Hosted Zone in Route 53**:
   ```bash
   aws route53 create-hosted-zone --name <your-domain-name> --caller-reference 1
   ```

2. **Set the DNS Name as an Environment Variable**:
   ```bash
   export KOPS_CLUSTER_NAME=<cluster-name>.<your-domain-name>
   ```

### **Step 6: Create the Kubernetes Cluster Configuration**

Now, create the cluster configuration:

```bash
kops create cluster --name=${KOPS_CLUSTER_NAME} --state=${KOPS_STATE_STORE} --zones=us-east-1a,us-east-1b,us-east-1c --node-count=2 --node-size=t3.medium --master-size=t3.medium --dns-zone=<your-domain-name> --ssh-public-key=~/.ssh/id_rsa.pub
```

### **Step 7: Create the Kubernetes Cluster**

Once the cluster configuration is created, you can create the cluster:

```bash
kops update cluster --name ${KOPS_CLUSTER_NAME} --yes
```

This command will create the necessary AWS infrastructure (VPC, subnets, EC2 instances, etc.) and set up Kubernetes on your instances.

### **Step 8: Validate the Cluster**

After the cluster is created, validate that it’s up and running:

```bash
kops validate cluster --name ${KOPS_CLUSTER_NAME}
```

You should see output indicating that your nodes are ready.

### **Step 9: Interact with Your Kubernetes Cluster**

You can now use `kubectl` to interact with your Kubernetes cluster:

```bash
kubectl get nodes
```

This will list all the nodes in your cluster, including the master and worker nodes.

### **Step 10: Deploy a Test Application (Optional)**

To ensure that your cluster is working correctly, deploy a simple application:

1. **Create a Deployment**:
   ```bash
   kubectl create deployment nginx --image=nginx
   ```

2. **Expose the Deployment as a Service**:
   ```bash
   kubectl expose deployment nginx --port=80 --type=LoadBalancer
   ```

3. **Get the Service Details**:
   ```bash
   kubectl get services
   ```

   This will provide you with an external IP address to access your Nginx deployment.

### **Step 11: Clean Up (Optional)**

If you want to delete the cluster later, you can do so with:

```bash
kops delete cluster --name ${KOPS_CLUSTER_NAME} --state=${KOPS_STATE_STORE} --yes
```

This command will tear down the cluster and remove all associated resources from AWS.

### **Conclusion**

You've successfully created a Kubernetes 3-node cluster using Kops on AWS EC2 instances running Ubuntu. This setup can be scaled and customized further based on your production needs.
