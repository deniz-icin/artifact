pipeline {
    agent any
    
    environment {
        SOURCE_DIR     = 'examples'
        BUCKET_NAME    = 'jenkins-artifact-bucket-deniz'
        AWS_REGION     = 'eu-north-1'
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
                    def sourceDir   = "${env.SOURCE_DIR}"
                    def zipFileName = "${env.BUILD_NUMBER}-artifacts.zip"
                    
                    sh 'echo "Creating zip archive for files under examples directory"'
                    sh "cd ${sourceDir} && zip -r ${zipFileName}"
                }
            }
        }
    
        stage('Push to S3') {
            steps {
                withAWS(credentials: "${env.CREDENTIALS_ID}", region: "${env.AWS_REGION}") {
                script {
                    def zipFileName = "${env.BUILD_NUMBER}-artifacts.zip"

                    sh 'echo "Uploading content with AWS creds"'
                    sh "aws s3 cp ${zipFileName} s3://${env.BUCKET_NAME}/${zipFileName}"
                }
            }
        }
    
    post {
        always {
            deleteDir()
        }
    }
}
}
}