pipeline {
  agent {
    kubernetes {
      label 'k8s'
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: build-node
spec:
  containers:
  - name: k8s-node
    image: gcr.io/oerik-test-project/jenkins-k8s-node:1.3.2
    imagePullPolicy: Always
    command:
    - cat
    tty: true
    volumeMounts:
    # Mount the docker.sock file so we can communicate wth the local docker
    # daemon
    - name: docker-sock-volume
      mountPath: /var/run/docker.sock
    # Mount the local docker binary
    - name: docker-bin-volume
      mountPath: /usr/bin/docker
    # Mount the jenkins project 's gcb service account key
  volumes:
  - name: docker-sock-volume
    hostPath:
      path: /var/run/docker.sock
  - name: docker-bin-volume
    hostPath:
      path: /usr/bin/docker
  # Create a volume that contains the jenkins gcb json key that was saved as a secret
"""
    }
  }


  stages {

    // stage('Checkout code') {
    //   steps {
    //     container('k8s-node') {
    //         checkout scm
    //     }
    //   }
    // }

    stage('test') {
      steps {
        container('k8s-node') {
           timeout(time: 10, unit: 'MINUTES') {
                sh '''
                  pwd
                  ls -l
                  virtualenv venv
                  source venv/bin/activate
                  pip install --editable .
                  mergeyaml --inpute test.yaml --set web.image.tag=1.0.4
                '''
          }
        }
      }
    }


  }

}
