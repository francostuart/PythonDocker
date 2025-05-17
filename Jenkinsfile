pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3' // Puedes ajustar la versión de Python que necesites
        VIRTUAL_ENV = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Environment') {
            steps {
                script {
                    // Instalar una versión específica de Python (si es necesario y el agente lo permite)
                    sh "python${PYTHON_VERSION} -m venv ${VIRTUAL_ENV}"
                    sh ". ${VIRTUAL_ENV}/bin/activate"
                    sh "python --version"
                    sh "pip --version"
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh ". ${VIRTUAL_ENV}/bin/activate"
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Linting') {
            steps {
                script {
                    sh ". ${VIRTUAL_ENV}/bin/activate"
                    // Ejemplo usando Flake8 para linting
                    sh 'pip install --upgrade pip setuptools wheel'
                    sh 'pip install flake8'
                    sh 'flake8 .'
                }
            }
        }

        stage('Testing') {
            steps {
                script {
                    sh ". ${VIRTUAL_ENV}/bin/activate"
                    // Ejemplo usando pytest para ejecutar las pruebas
                    sh 'pip install pytest'
                    sh 'pytest'
                    // O si tienes un archivo de configuración específico para pytest
                    // sh 'pytest -c pytest.ini'
                }
            }
        }

        stage('Build Package (Optional)') {
            steps {
                script {
                    sh ". ${VIRTUAL_ENV}/bin/activate"
                    sh 'pip install --upgrade pip setuptools wheel'
                    sh 'python setup.py sdist bdist_wheel'
                    sh 'ls dist/*.whl dist/*.tar.gz'
                }
            }
            // Condición para ejecutar esta etapa solo en la rama 'main' o 'master'
            when {
                branch 'main'
            }
        }

        /*stage('Publish Package (Optional)') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'pypi-credentials', usernameVariable: 'PYPI_USERNAME', passwordVariable: 'PYPI_PASSWORD')]) {
                        sh ". ${VIRTUAL_ENV}/bin/activate"
                        sh 'pip install twine'
                        sh "twine upload --repository pypi --username '${PYPI_USERNAME}' --password '${PYPI_PASSWORD}' dist/*"
                    }
                }
            }
            // Condición para ejecutar esta etapa solo en tags (releases)
            when {
                tag '*'
            }
        }*/
    }

    post {
        always {
            echo 'Pipeline finished'
        }
        success {
            echo 'Build succeeded'
        }
        failure {
            echo 'Build failed'
        }
    }
}