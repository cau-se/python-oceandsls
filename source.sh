# enable ANTLR support
# example
if [ -f /usr/local/lib/antlr-4.13.1-complete.jar ] && [ -f /usr/local/lib/antlrworks-1.5.2-complete.jar ]; then
    export CLASSPATH=".:/usr/local/lib/antlr-4.13.1-complete.jar:/usr/local/lib/antlrworks-1.5.2-complete.jar:$CLASSPATH"
    alias antlr4='java -jar /usr/local/lib/antlr-4.13.1-complete.jar'
    alias antlrworks='java -jar /usr/local/lib/antlrworks-1.5.2-complete.jar'
    alias grun='java org.antlr.v4.gui.TestRig'

    #export GRUN_CMD='java -cp ../:$CLASSPATH org.antlr.v4.gui.TestRig'
    export GRUN_CMD='java -cp .:../:/usr/local/lib/antlr-4.13.1-complete.jar:/usr/local/lib/antlrworks-1.5.2-complete.jar: org.antlr.v4.gui.TestRig'


    #Shows diagnostic output from lexer and parser if any
    #>diagrun exampleDsl example-dsl/exampleLSPServer prog example-dsl/input/test_Expr.expr
    diagrun() {
      pushd .  > /dev/null
      grammarName="${1}" # e.g. exampleDsl
      srcDir="${2}" # e.g. example-dsl/exampleLSPServer
      pkgName="${grammarName}"
      startRuleName="${3}" # e.g. prog
      testDataFile=`readlink -f $4` # e.g. example-dsl/input/test.odsl
      cd "${srcDir}/gen/java/${grammarName}"/ && ${GRUN_CMD} "${pkgName}"."${grammarName}" "${startRuleName}" -diagnostics < "${testDataFile}"
      popd > /dev/null
    }

    #Shows GUI parse tree browser
    #>guirun exampleDsl example-dsl/exampleLSPServer prog example-dsl/input/test_Expr.expr
    guirun() {
      pushd .  > /dev/null
      grammarName="${1}"
      srcDir="${2}"
      pkgName="${grammarName}"
      startRuleName="${3}"
      testDataFile=`readlink -f $4`
      cd "${srcDir}/gen/java/${grammarName}"/ && ${GRUN_CMD} "${pkgName}"."${grammarName}" "${startRuleName}" -gui < "${testDataFile}"
      popd > /dev/null
    }

    #Generates a PS of the parsetree
    #>psrun exampleDsl example-dsl/exampleLSPServer prog example-dsl/input/test_Expr.expr
    psrun() {
      pushd .  > /dev/null
      grammarName="${1}"
      srcDir="${2}"
      pkgName="${grammarName}"
      startRuleName="${3}"
      testDataFile=`readlink -f $4`
      cd "${srcDir}/gen/java/${grammarName}"/ && ${GRUN_CMD} "${pkgName}"."${grammarName}" "${startRuleName}" -ps "${testDataFile}".ps < "${testDataFile}"
      popd > /dev/null
    }

    #Shows tokens detected by lexer
    #>tokenrun exampleDsl example-dsl/exampleLSPServer prog example-dsl/input/test_Expr.expr
    tokenrun() {
      pushd .  > /dev/null
      grammarName="${1}"
      srcDir="${2}"
      pkgName="${grammarName}"
      startRuleName="${3}"
      testDataFile=`readlink -f $4`
      cd "${srcDir}/gen/java/${grammarName}"/ && ${GRUN_CMD} "${pkgName}"."${grammarName}" "${startRuleName}" -tokens < "${testDataFile}"
      popd > /dev/null
    }

    #Prints text tree output of parse tree
    #>treerun exampleDsl example-dsl/exampleLSPServer prog example-dsl/input/test_Expr.expr
    treerun() {
      pushd .  > /dev/null
      grammarName="${1}"
      srcDir="${2}"
      pkgName="${grammarName}"
      startRuleName="${3}"
      testDataFile=`readlink -f $4`
      cd "${srcDir}/gen/java/${grammarName}"/ && ${GRUN_CMD} "${pkgName}"."${grammarName}" "${startRuleName}" -tree < "${testDataFile}"
      popd > /dev/null
    }
    
    #Shows trace information when parsing input file
    #>tracerun exampleDsl example-dsl/exampleLSPServer prog example-dsl/input/test_Expr.expr
    tracerun() {
      pushd .  > /dev/null
      grammarName="${1}"
      srcDir="${2}"
      pkgName="${grammarName}"
      startRuleName="${3}"
      testDataFile=`readlink -f $4`
      cd "${srcDir}/gen/java/${grammarName}"/ && ${GRUN_CMD} "${pkgName}"."${grammarName}" "${startRuleName}" -trace < "${testDataFile}"
      popd > /dev/null
    }
fi