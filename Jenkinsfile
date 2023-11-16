pipeline {
    agent any
    parameters {
        choice(name: 'ENVIRONMENT', choices: 'Prod\nStage', description: 'Environment')
    }
    stages {
        stage('Set Environment Variables') {
            steps {
                script {
                    switch(env.ENVIRONMENT) {
                        case 'Prod':
                            env.DOMAIN = 'console.redhat.com'
                            withCredentials([usernamePassword(credentialsId: 'Prod-creds', passwordVariable: 'password', usernameVariable: 'username')]) {
                                env.USERNAME = "$username"
                                env.PASSWORD = "$password"
                            }
                            break
                        case 'Stage':
                            env.DOMAIN = 'console.stage.redhat.com'
                            env.HTTPS_PROXY = 'http://squid.corp.redhat.com:3128'
                            withCredentials([usernamePassword(credentialsId: 'stage-creds', passwordVariable: 'password', usernameVariable: 'username')]) {
                                env.USERNAME = "$username"
                                env.PASSWORD = "$password"
                            }
                            break 
                    }
                }
            }
        }
        stage('Test Suite') {
            steps {
                sh 'poetry run python -m pytest -s tests/test_dry_run.py '
            }
        }
    }
}
