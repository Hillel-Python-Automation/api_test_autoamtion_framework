pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Hillel-Python-Automation/api_test_autoamtion_framework.git'
            }
        }
        stage('Run tests') {
            agent {
                docker {
                    alwaysPull true
                    image 'yurigrbond88/api_python:latest'
//                     reuseNode true
                }
            }
            steps {
                sh 'pytest -rA --alluredir=allure-results'
            }
        }
        stage('Publish results') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }
}