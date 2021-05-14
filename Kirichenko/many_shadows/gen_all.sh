i=1
while read p; do
  echo "$i vector"
  echo "$i " >> result_performed_100_shadows_random_vecs_5_100.txt
  echo "$p" | python kir_one_shadow_performed_for_some_shadows.py >> result_performed_100_shadows_random_vecs_5_100.txt
  i=$(( $i + 1 ))
done < random_vecs_5_100.txt
echo 'n = 5 ended'
i=1
while read p; do
  echo "$i vector"
  echo "$i " >> result_performed_100_shadows_random_vecs_6_100.txt
  echo "$p" | python kir_one_shadow_performed_for_some_shadows.py >> result_performed_100_shadows_random_vecs_6_100.txt
  i=$(( $i + 1 ))
done < random_vecs_6_100.txt
echo 'n = 6 ended'
i=1
while read p; do
  echo "$i vector"
  echo "$i " >> result_performed_100_shadows_random_vecs_7_100.txt
  echo "$p" | python kir_one_shadow_performed_for_some_shadows.py >> result_performed_100_shadows_random_vecs_7_100.txt
  i=$(( $i + 1 ))
done < random_vecs_7_100.txt
echo 'n = 7 ended'
i=1
while read p; do
  echo "$i vector"
  echo "$i " >> result_performed_100_shadows_random_vecs_8_100.txt
  echo "$p" | python kir_one_shadow_performed_for_some_shadows.py >> result_performed_100_shadows_random_vecs_8_100.txt
  i=$(( $i + 1 ))
done < random_vecs_8_100.txt
echo 'n = 8 ended'
i=1
while read p; do
  echo "$i vector"
  echo "$i " >> result_performed_100_shadows_random_vecs_9_100.txt
  echo "$p" | python kir_one_shadow_performed_for_some_shadows.py>> result_performed_100_shadows_random_vecs_9_100.txt
  i=$(( $i + 1 ))
done < random_vecs_9_100.txt
echo 'n = 9 ended'
