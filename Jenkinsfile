pipeline {
  agent any

  environment {
    VENV_DIR = 'venv'
    IMAGE_NAME = 'my-python-app'
    IMAGE_TAG = 'latest'
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python Env') {
      steps {
        sh '''
          python3 -m venv $VENV_DIR
          . $VENV_DIR/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install flake8 pytest
        '''
      }
    }

    stage('Linting') {
      steps {
        sh '''
          . $VENV_DIR/bin/activate
          echo "Ejecutando flake8..."
          flake8 . --exclude=venv --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --exclude=venv --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
        '''
      }
    }

    stage('Testing') {
       steps{
        sh '''
          echo "Pendiente ejecucion de pytest..."
        '''
        }
      /*steps {
        sh '''
          . $VENV_DIR/bin/activate
          echo "Ejecutando pytest..."
          pytest --maxfail=1 --disable-warnings -q
        '''
      }*/
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          echo "Construyendo imagen Docker..."
          docker build --no-cache -t $IMAGE_NAME:$IMAGE_TAG .
        '''
      }
    }
  }

  post {
    always {
      echo '🏁 Pipeline finalizado'
    }
    success {
      echo '✅ Todo pasó correctamente'
    }
    failure {
      echo '❌ Falló alguna etapa'
    }
  }
}
