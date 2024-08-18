This file cosist of command for kubernetes cluster.

1> to check the version of kubectl
#kubectl version

2>To get nodes information
#kubectl get nodes

3>To create the pod in kubernetes
#kubectl create -f pod.yaml

4>To get the pod information
#kubectl get pods

5>To get the full information on running pods
#kubectl get pod -o wide

6>TO delete the pod
#kubectl delete pod "nameofthepod"

7>To create pod using apply
#kubectl apply -f pod.yaml

8>TO get the information on the pod 
#kubectl describe pod "nameofthepod"

9>TO get the logs of the pod
#kubectl logs nameofthepod
