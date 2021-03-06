#!/bin/bash
# This script executes start.sh on all the test pages, then make a summary of the result

if [ -z "$1" ]
  then
    echo -e "\nSyntax: ./test.sh destination_folder [python command]\n\n"
    exit
fi
match=$1

if [ -n "$2" ] ; then
  python="$2"
else
  python=""
fi

out=${match}_test.out

echo "-----------------------------------------------" >> $out
cat start.sh                                           >> $out
echo "-----------------------------------------------" >> $out
date                                                   >> $out
./start.sh pages/test $match "$python"
cat ${match}.out                                       >> $out
date                                                   >> $out
echo "-----------------------------------------------" >> $out

awk '
BEGIN{n_good=0; n_bad=0; n_mb=0;}
/maybe$/{n_mb=n_mb+1; next;}
/^yes_.*no$|^no_.*yes$/{n_bad=n_bad+1; next;}
/^yes_.*yes$|^no_.*no$/{n_good=n_good+1; next;}
END{
  printf("good: %d  %5.1f     bad: %d  %5.1f     mb: %d. %5.1f\n\n", n_good, 100*n_good/NR, n_bad, 100*n_bad/NR, n_mb, 100*n_mb/NR);
}
' $match.out                                           >> $out
