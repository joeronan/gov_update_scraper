touch ./output/most_recent.txt
start=$(head -n 1 ./output/most_recent.txt)
echo ${start}

while ! [[ ${runtype} =~ ^(d|l)$ ]] ; do
  echo Check past [d]ay or since [l]ast time? Last time: ${start}
  read runtype
done

if [[ $runtype == "d" ]]; then
  start=$(gdate --iso-8601='seconds' --date="-1 day")
fi

end=$(gdate --iso-8601='seconds')

python3 scrape.py ${start} ${end} "./output/${start}_${end}.csv"
python3 tidy.py "./output/${start}_${end}.csv" > ./output/most_recent.txt

sed -i.bak "1s/^/${start}\\n/g" output/most_recent.txt
sed -i.bak "1s/^/${end}\\n/g" output/most_recent.txt
rm output/most_recent.txt.bak