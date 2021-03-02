while read p; do
  echo "$p" | python3 find_min_poly.py
  echo "=============================="
done < data.txt

