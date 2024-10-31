export BASE_DIR=`dirname $BASH_SOURCE`
export P=`pwd`
export BASE_DIR=`(cd $BASE_DIR; pwd)`
cd "$P"

echo $BASE_DIR

git fetch
. ~/.venv/bin/activate
cd "$BASE_DIR/cp-dsl"
export PYTHONPATH="$BASE_DIR/cp-dsl"

# end
