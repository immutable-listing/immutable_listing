
python=mypython1
fs=(
    "$python compare.test.py"
    "$python make.test.py"
    "$python fill.test.py"
    "$python chunker_add.test.py"
    "$python sync.test.py"
    "$python glue.test.py"
)

for f in "${fs[@]}"
do
    echo '---------------------------------->' $f
    eval $f
    if [ $? -ne 0 ]; then
        break
    fi
done