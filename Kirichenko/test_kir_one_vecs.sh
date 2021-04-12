i=1
while read p; do
  echo "$i vector"
  echo "$i " >> result_random_vecs_3_100.txt
  echo "$p" | python kir.py >> result_random_vecs_3_100.txt
  i=$(( $i + 1 ))
done < random_vecs_3_100.txt

