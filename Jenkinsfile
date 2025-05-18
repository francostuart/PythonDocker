pipeline {
  agent {
    docker {
      image 'python:3.11-slim' // Usa imagen similar a la del Dockerfile
      args  '-u root:root' // evita problemas de permisos
    }
  }

  environment {
    VENV_DIR = 'venv'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install Tools') {
      steps {
        sh '''
          apt-get update
          apt-get install -y git build-essential
        '''
      }
    }

    stage('Set Up Virtual Env') {
      steps {
        sh '''
          python -m venv $VENV_DIR
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
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
        '''
      }
    }

    stage('Testing') {
      steps {
        sh '''
          . $VENV_DIR/bin/activate
          pytest --maxfail=1 --disable-warnings -q
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          docker build -t my-python-app:latest .
        '''
      }
    }

    stage('Push & Deploy (Render)') {
      when {
        branch 'main'
      }
      steps {
        echo 'Aquí puedes usar render.yaml o curl a la API de Render para desplegar'
      }
    }
  }

  post {
    success {
      echo '✅ Todo pasó correctamente'
    }
    failure {
      echo '❌ Falló alguna etapa'
    }
    always {
      echo '🏁 Pipeline finalizado'
    }
  }
}
