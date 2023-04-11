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
    stage('Docker prune') {
      steps {
        sh 'docker image prune --all'
      }
    }
    stage('Start container') {
      steps {
        sh 'docker compose up -d --build'
        sh 'docker compose ps'
      }
    }
  }
}
