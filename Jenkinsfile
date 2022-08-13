pipeline {
  agent any
  stages {
    stage("verify tooling") {
      steps {
        sh '''
          docker version
        '''
      }
    }
    stage('Start container') {
      steps {
        sh 'docker compose up -d --build celery cache'
        sh 'docker compose ps'
      }
    }
  }
}
