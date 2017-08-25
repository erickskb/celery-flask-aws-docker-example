node("DG") {

   // Wipe the workspace so we are building completely clean
   deleteDir()

   // Mark the code checkout 'stage'....
   stage 'Checkout'

   // Checkout code from repository
   checkout scm

   sh '''#!/usr/bin/env bash
         mkdir .cache .pylint.d results
         chmod 777 .cache  .pylint.d results
      '''
   stage 'Code Quality'
   docker.image('registry-dev.discover.digitalglobe.com/centos7python27').inside {
               sh '''#!/usr/bin/env bash
                     echo $CLIENT_ID
                     echo $CLIENT_SECRET
                     export PYENV_HOME=`pwd`
                     virtualenv --no-site-packages $PYENV_HOME
                     . $PYENV_HOME/bin/activate
                     pip install pytest pytest-cov pytest-html pylint pep8
                     pylint -f parseable ./service/ | tee ./results/pylint.out
                     pep8 ./service/ --ignore=E501 | tee ./results/pep8.out
                  '''
   }  

   stage 'Unit Testing'
   docker.image('registry-dev.discover.digitalglobe.com/centos7python27').inside {
                    withEnv([
                        'npm_config_cache=npm-cache',
                        'HOME=.',
                        ]) {
                        sh '''#!/usr/bin/env bash
                              export PYENV_HOME=`pwd`
                              virtualenv --no-site-packages $PYENV_HOME
                              . $PYENV_HOME/bin/activate
                              pip install pytest pytest-cov pytest-html
                              pip install --find-links=vendor/ -r requirements.txt
                              py.test ./test/unit_tests --cov ./service/ --cov-report term-missing --cov-report xml --junitxml=./results/junit.xml --html=./results/index.html
                           '''
                    }
   }

   stage 'Deploy POC'
   docker.image('registry-dev.discover.digitalglobe.com/centos7python27').inside {
   }


}
