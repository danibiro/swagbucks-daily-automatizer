if [ ! $# -eq 1 ]
then
    echo Usage: $0 path_to_py_file
    exit 1
fi

if [ ! -d $1 ]
then
    echo $1 is not a valid directory
    exit 1
fi

if [ ! -e "$1/main.py" ]
then
    echo There is no file named main.py in the directory $1
    exit 1
fi

cd $1
/usr/bin/python3.10 main.py