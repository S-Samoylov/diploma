k=1
while read m; do
	i=1
	echo "$k vector"
	while read p; do
		echo "$i shadow"
		echo "$i " >> 'n_100vecs_all_shadows/result_vec_100_n_3_all_shadows.txt'
		echo -e "$m\n$p" | python kir_one_shadow_for_shadows.py >> 'n_100vecs_all_shadows/result_vec_100_n_3_all_shadows.txt'
		i=$(( $i + 1 ))
	done < n_3_all_shadows.txt
	k=$(( $k + 1 ))
done < random_vecs_3_100.txt

