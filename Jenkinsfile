pipeline {
    agent any

    environment {
        REPO_URL     = 'github.com/MarCOCO999/actividad-doxygen.git'
        NOTIFY_EMAIL = 'marco.contreras002@gmail.com'
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

        stage('Check Documentation') {
            steps {
                echo 'Verificando el estado de la documentación...'
                script {
                    if (!fileExists('docs/html/index.html')) {
                        error('ALERTA: la documentación no se generó (falta docs/html/index.html)')
                    }
                    def advertencias = sh(
                        script: "grep -i 'warning' doxygen-warnings.log 2>/dev/null | grep -vi 'output language' | wc -l",
                        returnStdout: true
                    ).trim().toInteger()
                    echo "Advertencias de documentación encontradas: ${advertencias}"
                    if (advertencias > 0) {
                        unstable("Doxygen reportó ${advertencias} advertencia(s) de documentación")
                    }
                }
                archiveArtifacts artifacts: 'doxygen-warnings.log', allowEmptyArchive: true
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
        unstable {
            mail to: env.NOTIFY_EMAIL,
                 subject: "[Jenkins] ADVERTENCIA en ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "La documentación se generó con advertencias.\nRevisar: ${env.BUILD_URL}\nEl detalle está en el artefacto doxygen-warnings.log."
        }
        failure {
            mail to: env.NOTIFY_EMAIL,
                 subject: "[Jenkins] FALLO en ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "El pipeline falló. Revisar la etapa con error en: ${env.BUILD_URL}console"
        }
        fixed {
            mail to: env.NOTIFY_EMAIL,
                 subject: "[Jenkins] CORREGIDO ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "El pipeline volvió a funcionar correctamente: ${env.BUILD_URL}"
        }
    }
}