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

            withCredentials([string(credentialsId: 'telegramToken', variable: 'TOKEN'),
                string(credentialsId: 'telegramChatId', variable: 'CHAT_ID')]){
            sh  '''curl -s -X POST https://api.telegram.org/bot"$TOKEN"/sendMessage -d chat_id="$CHAT_ID" -d text="Your build $JOB_NAME-$BUILD_NUMBER is finished"'''
                }
        }
        
        success {
            echo 'Model is trained and deployed!'
            
            withCredentials([string(credentialsId: 'telegramToken', variable: 'TOKEN'),
                string(credentialsId: 'telegramChatId', variable: 'CHAT_ID')]){
            sh  '''curl -s -X POST https://api.telegram.org/bot"$TOKEN"/sendMessage -d chat_id="$CHAT_ID" -d text="And It worked! :D" '''
                }
            }
        failure {
            echo 'Something went badly wrong!'
            
            withCredentials([string(credentialsId: 'telegramToken', variable: 'TOKEN'),
                string(credentialsId: 'telegramChatId', variable: 'CHAT_ID')]){
            sh  '''curl -s -X POST https://api.telegram.org/bot"$TOKEN"/sendMessage -d chat_id="$CHAT_ID" -d text="But it failed :(" '''
                }
                          }
            }
        }
 