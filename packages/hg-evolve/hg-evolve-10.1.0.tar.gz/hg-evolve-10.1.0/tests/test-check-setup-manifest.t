#require test-repo check-manifest

  $ cat << EOF >> $HGRCPATH
  > [experimental]
  > evolution=all
  > EOF

Run check manifest:

  $ cd $TESTDIR/..
  $ check-manifest
  lists of files in version control and sdist match
