echo Module code:
find pymarshal -type f -name '*.py' -exec cat {} \; | wc -l

echo Test code:
find test -type f -name '*.py' -exec cat {} \; | wc -l

echo Total:
find pymarshal test -type f -name '*.py' -exec cat {} \; | wc -l
