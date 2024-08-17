Kubernetes 3 node deployment on Ec2Instance Ubuntu:->

Creating a production-grade Kubernetes cluster on EC2 instances with Ubuntu involves several steps, including setting up the infrastructure, configuring networking, and installing and configuring Kubernetes components. Here's a step-by-step guide to help you set up a Kubernetes cluster on AWS using EC2 instances running Ubuntu.

### **Prerequisites**

1. **AWS Account**: Ensure you have access to an AWS account with appropriate permissions.
2. **AWS CLI**: Install and configure the AWS CLI on your local machine.
3. **EC2 Key Pair**: Create an EC2 key pair to SSH into your instances.

### **Step 1: Provision EC2 Instances**

1. **Create EC2 Instances**:
   - Launch at least three EC2 instances (one master and two or more worker nodes).
   - Choose the Ubuntu Server AMI (preferably the latest LTS version).
   - Select an instance type based on your expected workload (e.g., `t3.medium` for a small cluster).
   - Configure network settings, ensuring that instances are in the same VPC and subnet.
   - Enable ports for SSH (22), Kubernetes API server (6443), and any other required ports.
   - Attach the key pair you created for SSH access.

2. **Tag Instances**:
   - Tag the master node with `Role=master`.
   - Tag worker nodes with `Role=worker`.

### **Step 2: Prepare the EC2 Instances**

1. **Update and Install Dependencies**:
   - SSH into each instance using the key pair and run the following commands:
     ```bash
     sudo apt-get update
     sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
     ```

2. **Disable Swap**:
   - Kubernetes requires swap to be disabled:
     ```bash
     sudo swapoff -a
     sudo sed -i '/ swap / s/^/#/' /etc/fstab
     ```

3. **Configure Kernel Parameters**:
   - Set up sysctl parameters for Kubernetes networking:
     ```bash
     cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
     net.bridge.bridge-nf-call-iptables = 1
     net.bridge.bridge-nf-call-ip6tables = 1
     net.ipv4.ip_forward = 1
     EOF
     sudo sysctl --system
     ```

### **Step 3: Install Docker**

1. **Install Docker on All Nodes**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

### **Step 4: Install Kubernetes Components**

1. **Add the Kubernetes APT Repository**:
   ```bash
   curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
   sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
   ```

2. **Install `kubeadm`, `kubelet`, and `kubectl` on All Nodes**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y kubelet kubeadm kubectl
   sudo apt-mark hold kubelet kubeadm kubectl
   ```

### **Step 5: Initialize the Kubernetes Master Node**

1. **Initialize the Cluster**:
   - On the master node, run the following command:
     ```bash
     sudo kubeadm init --pod-network-cidr=10.244.0.0/16
     ```
   - Note the `kubeadm join` command displayed at the end of the initialization; you’ll need this to join worker nodes.

2. **Set Up `kubectl` for the Local User**:
   ```bash
   mkdir -p $HOME/.kube
   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   sudo chown $(id -u):$(id -g) $HOME/.kube/config
   ```

### **Step 6: Deploy a Pod Network**

1. **Install a Pod Network (e.g., Flannel)**:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
   ```

### **Step 7: Join Worker Nodes to the Cluster**

1. **Join the Worker Nodes**:
   - On each worker node, run the `kubeadm join` command you noted from the master node setup:
     ```bash
     sudo kubeadm join <master-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
     ```

### **Step 8: Verify the Cluster**

1. **Check Node Status**:
   - On the master node, verify that all nodes have joined and are in a `Ready` state:
     ```bash
     kubectl get nodes
     ```

### **Step 9: Install Additional Tools (Optional)**

1. **Install Metrics Server**:
   - The Metrics Server collects resource usage data from the nodes and pods:
     ```bash
     kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
     ```

2. **Install a Kubernetes Dashboard**:
   - To install the Kubernetes dashboard for visual management:
     ```bash
     kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml
     ```

### **Step 10: Set Up Persistent Storage (Optional)**

1. **Configure Persistent Volumes**:
   - Set up persistent storage using AWS EBS volumes or any other storage solution.

### **Step 11: Configure High Availability (Optional)**

1. **Set Up Multiple Master Nodes**:
   - For high availability, consider setting up multiple master nodes with etcd clusters.
   - Use a load balancer for the Kubernetes API server.

### **Conclusion**

You now have a production-grade Kubernetes cluster running on Ubuntu EC2 instances. This setup is scalable and can be customized further depending on your specific requirements. You can also integrate CI/CD pipelines, monitoring, and logging tools to enhance your cluster's capabilities.
