pipeline {
    agent any

    environment {
        // CAMBIAR por tu usuario y nombre de repositorio (sin https://)
        REPO_URL = 'github.com/MarCOCO999/actividad-doxygen.git'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Creando entorno virtual e instalando dependencias...'
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install --upgrade pip
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                sh 'venv/bin/python -m pytest -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Generate Documentation') {
            steps {
                echo 'Generando documentación con Doxygen...'
                sh 'doxygen Doxyfile'
                archiveArtifacts artifacts: 'docs/html/**', fingerprint: true
            }
        }

        stage('Version Control') {
            steps {
                echo 'Subiendo la documentación generada al repositorio...'
                withCredentials([usernamePassword(credentialsId: 'github-token',
                                                  usernameVariable: 'GIT_USER',
                                                  passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        git config user.name "Jenkins CI"
                        git config user.email "jenkins@localhost"
                        git add docs
                        if git diff --cached --quiet; then
                            echo "La documentación no tiene cambios."
                        else
                            git commit -m "docs: actualización automática (build #${BUILD_NUMBER})"
                            git push https://${GIT_USER}:${GIT_TOKEN}@${REPO_URL} HEAD:main
                        fi
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Desplegando la aplicación en el entorno de prueba (puerto 5000)...'
                sh '''
                    if [ -f flask.pid ]; then kill $(cat flask.pid) || true; fi
                    JENKINS_NODE_COOKIE=dontKillMe nohup venv/bin/python app.py > flask.log 2>&1 &
                    echo $! > flask.pid
                    sleep 5
                    curl -f "http://localhost:5000/hello?name=Jenkins"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completado: código probado, documentación generada y app desplegada.'
        }
        failure {
            echo 'ALERTA: el pipeline falló. Revisar la etapa con error.'
        }
    }
}
