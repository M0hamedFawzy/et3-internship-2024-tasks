kubectl apply -f ./k8s/nginx/persistent-volume.yml
kubectl apply -f ./k8s/nginx/persistent-volume-claim.yml
kubectl apply -f ./k8s/nginx/persistent-volume-static.yml
kubectl apply -f ./k8s/nginx/persistent-volume-claim-static.yml
kubectl delete --ignore-not-found -f ./k8s/nginx/deployment.yml
kubectl apply -f ./k8s/nginx/deployment.yml
kubectl apply -f ./k8s/nginx/service.yml

kubectl apply -f ./k8s/postgres/persistent-volume.yml
kubectl apply -f ./k8s/postgres/persistent-volume-claim.yml
kubectl apply -f ./k8s/postgres/deployment.yml
kubectl apply -f ./k8s/postgres/service.yml

kubectl apply -f ./k8s/rabbit/persistent-volume.yml
kubectl apply -f ./k8s/rabbit/persistent-volume-claim.yml
kubectl delete --ignore-not-found -f ./k8s/rabbit/deployment.yml
kubectl apply -f ./k8s/rabbit/deployment.yml
kubectl apply -f ./k8s/rabbit/service.yml
kubectl apply -f ./k8s/rabbit/service-external.yml
kubectl apply -f ./k8s/rabbit/ingress.yml

kubectl apply -f ./k8s/app/persistent-volume.yml
kubectl apply -f ./k8s/app/persistent-volume-claim.yml
kubectl delete --ignore-not-found -f ./k8s/app/deployment.yml
kubectl apply -f ./k8s/app/deployment.yml
kubectl apply -f ./k8s/app/service.yml
kubectl apply -f ./k8s/app/ingress.yml

kubectl delete --ignore-not-found -f ./k8s/celery/deployment-worker.yml
kubectl apply -f ./k8s/celery/deployment-worker.yml

kubectl delete --ignore-not-found -f ./k8s/celery/deployment-beat.yml
kubectl apply -f ./k8s/celery/deployment-beat.yml