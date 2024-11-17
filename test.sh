set -e
if [ -z $1 ]; then
    echo Empty argument
fi
python useful/remove_xattrs.py $1 sha256
python make.py $1 m
echo '{"": {"hash": "sha256", "bs": 8192}}' > ch
python fill.py $1 m sha256 chunker ch 128