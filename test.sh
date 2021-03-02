while read p; do
  echo "$p" | python find_min_poly.py
  echo "=============================="
done < data.txt

