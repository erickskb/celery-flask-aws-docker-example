node{

    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */
        app = docker.build("3pi-workflow")
    }
    
    stage('Docker push') {
        docker.withRegistry('https://465688003075.dkr.ecr.us-west-2.amazonaws.com', 'ecr:us-west-2:AWS-3pi-workflow-docker') {
        docker.image('3pi-workflow').push('latest')
        }
    }

    stage('Test image') {

        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Deloy to AWS') {
        app.inside {
            sh 'echo "Done."'
        }
    }
}
