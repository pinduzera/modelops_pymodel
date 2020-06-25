pipeline {
  agent any
  environment {
  PATH = "/opt/anaconda3/bin/:$PATH"
  }
  
    options {
        timeout(time: 15, unit: 'MINUTES')   // timeout on whole pipeline job
    }

    stages {
      stage('Check Data') {
        steps {
          sh "python verify_tables_iris.py"
            }
          }
      stage('Model Training & Validation') {
        steps {
          sh "python training_code_iris.py"
                }
          }
    stage('Model Upload & publish') {
        steps {
          sh "python upload_model_iris.py"

                }
          }
      stage('Testing Publication') {
        steps {
          sh "python pub_test.py"

                }
          }
            
        
    }
      post {
        always {
            cleanWs deleteDirs: true, notFailBuild: true
            echo 'The job is done!'
            telegramSend("message": "test message")
        }
        
        success {
            echo 'Model is trained and deployed!'
        }
        failure {
            echo 'Something went badly wrong!'
        }
    }

}