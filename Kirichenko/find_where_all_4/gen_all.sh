i=1
while read p; do
  echo "$i vector"
  echo "$i " >> result_performed_48_shadows_random_vecs_4_100.txt
  echo "$p" | python kir_one_shadow_performed_for_some_shadows.py >> result_performed_48_shadows_random_vecs_4_100.txt
  i=$(( $i + 1 ))
done < random_vecs_4_100.txt
echo 'n = 4 ended'
