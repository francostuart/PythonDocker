pipeline {
  agent any

  environment {
    VENV_DIR    = 'venv'
    IMAGE_NAME  = 'my-python-app'
    //IMAGE_TAG   = "${BUILD_NUMBER}"
    IMAGE_TAG = ''
    DOCKER_REPO = 'rbueno23/my-python-app'  // <–– ajusta aquí
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
        }
    }

    //debug branch
    stage('Debug Branch') {
       steps {
         sh 'echo "BRANCH_NAME=$BRANCH_NAME"'
         sh 'git rev-parse --abbrev-ref HEAD'
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

    /*stage('Get Version') {
      steps {
        script {
          // 1) Listamos y cat para ver caracteres invisibles
          sh '''
            echo ">>> Listando workspace:"
            ls -l .
            echo ">>> Contenido crudo de version.txt (con cat -v para ver BOM/CRLF):"
            cat -v version.txt || true
          '''

          // 2) Leemos con readFile y mostramos longitud
          def raw = readFile('version.txt')
          echo "Raw readFile: '${raw}' (longitud=${raw.length()})"

          // 3) Hacemos trim() y volvemos a medir
          def version = raw.trim()
          echo "Trimmed version: '${version}' (longitud=${version.length()})"

          // 4) Fallamos si sigue vacío
          if (!version) {
            error "❌ version.txt está vacío o tiene sólo espacios/CRLF/BOM."
          }

          // 5) Asignamos a la variable de entorno
          env.IMAGE_TAG = version
          echo "✅ Usando versión según código: ${env.IMAGE_TAG}"
        }
      }
    }*/

    stage('Build Docker Image') {
      steps {
        script {

          // 1. Leemos la versión
          def version = readFile('version.txt').trim()
          if (!version) {
            error "❌ version.txt está vacío o no existe"
          }
          echo "✅ Versión leída: ${version}"

            sh """
              echo "Construyendo imagen Docker..."
              docker build --no-cache -t ${IMAGE_NAME}:${version} .
            """
        }
      }
    }


    // … Checkout, Setup, Linting, Testing, Build Docker Image …
    stage('Push Docker Image') {
      when { branch 'multibranch' } //comentado para modo pipeline, en multibranch si funciona
      steps {
        script{

            // 1. Leemos la versión
            def version = readFile('version.txt').trim()
            if (!version) {
                error "❌ version.txt está vacío o no existe"
            }
            echo "✅ Versión leída: ${version}"

            withCredentials([usernamePassword(
              credentialsId: 'dockerhub-creds',
              usernameVariable: 'DOCKER_USER',
              passwordVariable: 'DOCKER_PASS'
            )]) {
              sh """
                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                docker tag ${IMAGE_NAME}:latest ${DOCKER_REPO}:${version}
                docker push ${DOCKER_REPO}:${version}
              """
            }
        }
      }
    }


    stage('Deploy to Render') {
      when { branch 'multibranch' }
      steps {
        withCredentials([string(
          credentialsId: 'render-api-key',
          variable: 'RENDER_API_KEY'
        )]) {
          sh '''
            echo "Triggering deploy on Render..."
            curl -X POST https://api.render.com/deploy/srv-d0k4vube5dus73bfckn0?key=YRPtr7tzvnE \
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
