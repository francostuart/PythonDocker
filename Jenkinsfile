pipeline {
  agent any

  environment {
    VENV_DIR    = 'venv'
    IMAGE_NAME  = 'my-python-app'
    IMAGE_TAG   = 'latest'
    DOCKER_REPO = 'rbueno23/my-python-app'  // <–– ajusta aquí
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


    // … Checkout, Setup, Linting, Testing, Build Docker Image …
    stage('Push Docker Image') {
      when { branch 'main' }
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'dockerhub-creds',
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS'
        )]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker tag $IMAGE_NAME:$IMAGE_TAG $DOCKER_REPO:$IMAGE_TAG
            docker push $DOCKER_REPO:$IMAGE_TAG
          '''
        }
      }
    }


    stage('Deploy to Render') {
      when { branch 'main' }
      steps {
        withCredentials([string(
          credentialsId: 'render-api-key',
          variable: 'RENDER_API_KEY'
        )]) {
          sh '''
            echo "Triggering deploy on Render..."
            curl -X POST https://api.render.com/deploy/srv-d0k4vube5dus73bfckn0/deploys \
              -H "Accept: application/json" \
              -H "Authorization: Bearer $RENDER_API_KEY" \
              -H "Content-Type: application/json" \
              -d '{"clearCache": false}'
          '''
        }
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
