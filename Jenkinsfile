#!/usr/bin/env groovy

pipeline {
  agent { label 'executor-v2' }

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '30'))
  }

  stages {
    stage('Run tests') {
      steps {
        sh './test.sh'
      }
      post { always {
        junit 'artifacts/pytest.xml, artifacts/TESTS-*'  // unit and feature test reports
        cobertura coberturaReportFile: 'artifacts/coverage.xml'
      }}
    }
  }

  post {
    always {
      cleanupAndNotify(currentBuild.currentResult)
    }
  }
}