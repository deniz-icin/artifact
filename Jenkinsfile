pipeline {
    agent any
    
    environment {
        SOURCE_DIR                 = 'examples'
        BUCKET_NAME                = 'jenkins-hermit-artifacts-zip'
        AWS_DEFAULT_REGION         = 'eu-north-1'
    }

    stages {
        stage('Clone Repo') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: 'https://github.com/facebookexperimental/hermit']]])
                }
            }
        }
    
        stage('Zip Artifacts') {
            steps {
                script {
                    def zipFileName = "${env.BUILD_NUMBER}-hermit-artifacts.zip"
                    
                    sh "zip -r ${zipFileName} ${env.SOURCE_DIR}"
                    sh "echo 'Zip archive for files under examples directory'"
                }
            }
        }
    
        stage('Push to S3') {
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_JENKINS_S3_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_JENKINS_S3_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]){
                script {
                    def zipFileName = "${env.BUILD_NUMBER}-hermit-artifacts.zip"
                    
                    sh "echo 'Uploading content with AWS creds'"
                    sh "/usr/local/bin/aws s3 cp ${zipFileName} s3://$BUCKET_NAME"
                }
            }
        }
    }
  }

    post {
        always {
            sh "rm -rf *"
        }
    }
}