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
          sh "python verify_tables.py"
            }
          }
      stage('Model Training') {
        steps {
          sh "python training_code.py"
                }
          }
/*
      stage('Model Validation') {
        steps {
          sh "Rscript --vanilla model_validation.R"
                }
          }
      stage('Testing Score Code') {
        steps {
          sh "Rscript --vanilla scoreTesting.R"
                }
          }
      stage('Model Upload & publish') {
        steps {
          sh "python upload_model.py"

                }
          }
      stage('Testing Publication') {
        steps {
          sh "python test_pub.py"

                }
          }
*/            
        
    }
      post { 
        always {
            cleanWs deleteDirs: true, notFailBuild: true
            echo 'The job is done!'
        }
        success {
            echo 'Model is trained and deployed!'
        }
        failure {
            echo 'Something went badly wrong!'
        }
    }

}