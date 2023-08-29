pipeline {
    agent any
    
    environment {
        SOURCE_DIR     = 'examples'
        BUCKET_NAME    = 'jenkins-artifact-bucket-deniz'
        CREDENTIALS_ID = 'b65ed143-2601-406c-85c1-c7c8e81f59f3'
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
                    def zipFileName = "${env.BUILD_NUMBER}-artifacts.zip"
                    
                    sh 'echo "Creating zip archive for files under examples directory"'
                    sh "zip -r ${zipFileName} ${env.SOURCE_DIR}"
                }
            }
        }
    
        stage('Push to S3') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.CREDENTIALS_ID}"
                ]]) {
                script {
                    def zipFileName = "${env.BUILD_NUMBER}-artifacts.zip"

                    sh 'echo "Uploading content with AWS creds"'
                    sh "/usr/local/bin/aws s3 cp ${zipFileName} s3://$BUCKET_NAME"
                }
            }
        }
    }
  }
}