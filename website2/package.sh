# run this to package the site and ready for deployment
rm lambda.zip
root_dir=$(pwd)
venv_dir="$root_dir/venv/lib/python3.8/site-packages"
cd $venv_dir && zip -r9 "$root_dir/lambda.zip" . \
&& cd "$root_dir/app" && zip -g ../lambda.zip -r .
