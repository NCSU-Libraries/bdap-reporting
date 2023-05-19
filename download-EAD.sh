while IFS= read line; do
URLpath=${line#https://www.lib.ncsu.edu/findingaids/}
NAME=${URLpath%/ead}.xml
echo "$line"
wget -O $NAME "$line"
done < /src/ead.txt
