traits define demo：
~~~yaml
name: demo
rules:
- name: never-restart
  path: .spec.template.spec.restartPolicy
  value: Never
  action: replace
- name: upper-name
  path: .spec.template.spec.containers.0.name
  value: Upper
  action: function
- name: default-tag
  path: .spec.template.spec.containers.0.image
  value: :latest
  action: concat
- name: default-env
  path: .spec.template.spec.containers.0.env
  value: 
    - name: PYTHONUNBUFFERD
      value: 1
  action: extend
~~~

template demo：
~~~yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: hello
spec:
  template:
    spec:
      containers:
      - name: hello
        image: busybox
        command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']
      restartPolicy: OnFailure

~~~

apply trais on template
```shell
traits traits.yaml job.yaml | yp -y
```

~~~yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: hello
spec:
  template:
    spec:
      containers:
        - name: HELLO
          image: busybox:latest
          command:
            - sh
            - -c
            - echo "Hello, Kubernetes!" && sleep 3600
          env:
            - name: PYTHONUNBUFFERD
              value: 1
      restartPolicy: Never
~~~
