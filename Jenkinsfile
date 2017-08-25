node("DG") {

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
