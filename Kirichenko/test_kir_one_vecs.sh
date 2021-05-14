i=1
while read p; do
  echo "$i vector"
  echo "$i " >> result_performed_random_vecs_9_100.txt
  echo "$p" | python kir_one_shadow_performed.py >> result_performed_random_vecs_9_100.txt
  i=$(( $i + 1 ))
done < random_vecs_9_100.txt

