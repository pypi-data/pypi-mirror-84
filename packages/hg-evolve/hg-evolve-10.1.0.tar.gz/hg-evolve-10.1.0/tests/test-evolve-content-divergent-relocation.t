======================================================
Tests the resolution of content divergence: relocation
======================================================

This file intend to cover case where changesets need to be moved to different parents

  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc|firstline}\n ({bookmarks}) [{branch}] {phase}"
  > [phases]
  > publish = False
  > [extensions]
  > rebase =
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH


Testing resolution of content-divergent changesets when they are on different
parents and resolution and relocation wont result in conflicts
------------------------------------------------------------------------------

  $ hg init multiparents
  $ cd multiparents
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg up .^^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo bar > b
  $ hg amend
  2 new orphan changesets

  $ hg rebase -r b1661037fa25 -d 8fa14d15e168 --hidden --config experimental.evolution.allowdivergence=True
  rebasing 2:b1661037fa25 "added b"
  2 new content-divergent changesets

  $ hg glog
  *  6:da4b96f4a8d6 added b
  |   () [default] draft
  | @  5:7ed0642d644b added b
  | |   () [default] draft
  | | *  4:c41c793e0ef1 added d
  | | |   () [default] draft
  | | *  3:ca1b80f7960a added c
  | | |   () [default] draft
  | | x  2:b1661037fa25 added b
  | |/    () [default] draft
  | o  1:c7586e2a9264 added a
  |/    () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[5] added b
  with: [6] added b
  base: [2] added b
  rebasing "other" content-divergent changeset da4b96f4a8d6 on c7586e2a9264
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at e7fdc662d630

  $ hg glog
  @  8:e7fdc662d630 added b
  |   () [default] draft
  | *  4:c41c793e0ef1 added d
  | |   () [default] draft
  | *  3:ca1b80f7960a added c
  | |   () [default] draft
  | x  2:b1661037fa25 added b
  |/    () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID e7fdc662d6305fee2908c3f1630e0b20d6f4689a
  # Parent  c7586e2a92645e473645847a7b69a6dc52be4276
  added b
  
  diff -r c7586e2a9264 -r e7fdc662d630 b
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/b	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +bar

  $ hg debugobsolete
  b1661037fa25511d0b7ccddf405e336f9d7d3424 7ed0642d644bb9ad93d252dd9ffe7b4729febe48 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  b1661037fa25511d0b7ccddf405e336f9d7d3424 da4b96f4a8d610a85b225583138f681d67e275dd 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  da4b96f4a8d610a85b225583138f681d67e275dd 11f849d7159fa30a63dbbc1a6d251a8d996baeb5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7ed0642d644bb9ad93d252dd9ffe7b4729febe48 e7fdc662d6305fee2908c3f1630e0b20d6f4689a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'evolve', 'user': 'test'}
  11f849d7159fa30a63dbbc1a6d251a8d996baeb5 e7fdc662d6305fee2908c3f1630e0b20d6f4689a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'evolve', 'user': 'test'}
  $ hg obslog --all
  @    e7fdc662d630 (8) added b
  |\     amended(content) from 11f849d7159f using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |    rewritten from 7ed0642d644b using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  11f849d7159f (7) added b
  | |    rebased(parent) from da4b96f4a8d6 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  7ed0642d644b (5) added b
  | |    amended(content) from b1661037fa25 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  da4b96f4a8d6 (6) added b
  |/     rebased(parent) from b1661037fa25 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  b1661037fa25 (2) added b
  

Resolving orphans to get back to a normal graph

  $ hg evolve --all
  move:[3] added c
  atop:[8] added b
  move:[4] added d
  $ hg glog
  o  10:be5a8b9faa8a added d
  |   () [default] draft
  o  9:e2ce33033e42 added c
  |   () [default] draft
  @  8:e7fdc662d630 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

More testing!

  $ echo x > x
  $ hg ci -Aqm "added x"
  $ hg glog -r .
  @  11:801b5920c7ea added x
  |   () [default] draft
  ~

  $ echo foo > x
  $ hg branch bar
  marked working directory as branch bar
  (branches are permanent and global, did you want a bookmark?)
  $ hg amend -m "added foo to x"

  $ hg up 'predecessors(.)' --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 801b5920c7ea
  (hidden revision '801b5920c7ea' was rewritten as: 5cf74a13db18)
  working directory parent is obsolete! (801b5920c7ea)
  (use 'hg evolve' to update to its successor: 5cf74a13db18)
  $ hg rebase -r . -d 'desc("added d")' --config experimental.evolution.allowdivergence=True
  rebasing 11:801b5920c7ea "added x"
  2 new content-divergent changesets

  $ hg glog
  @  13:45e15d6e88f5 added x
  |   () [default] draft
  | *  12:5cf74a13db18 added foo to x
  | |   () [bar] draft
  o |  10:be5a8b9faa8a added d
  | |   () [default] draft
  o |  9:e2ce33033e42 added c
  |/    () [default] draft
  o  8:e7fdc662d630 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[12] added foo to x
  with: [13] added x
  base: [11] added x
  rebasing "divergent" content-divergent changeset 5cf74a13db18 on be5a8b9faa8a
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 618f8bd245a8

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Branch bar
  # Node ID 618f8bd245a8d1892954eb49a88a6ec5e500a5b5
  # Parent  be5a8b9faa8af54f115aa168a2c8564acb40c37d
  added foo to x
  
  diff -r be5a8b9faa8a -r 618f8bd245a8 x
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/x	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +foo

The above `hg exp` and the following log call demonstrates that message, content
and branch change is preserved in case of relocation
  $ hg glog
  @  15:618f8bd245a8 added foo to x
  |   () [bar] draft
  o  10:be5a8b9faa8a added d
  |   () [default] draft
  o  9:e2ce33033e42 added c
  |   () [default] draft
  o  8:e7fdc662d630 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg debugobsolete
  b1661037fa25511d0b7ccddf405e336f9d7d3424 7ed0642d644bb9ad93d252dd9ffe7b4729febe48 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  b1661037fa25511d0b7ccddf405e336f9d7d3424 da4b96f4a8d610a85b225583138f681d67e275dd 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  da4b96f4a8d610a85b225583138f681d67e275dd 11f849d7159fa30a63dbbc1a6d251a8d996baeb5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7ed0642d644bb9ad93d252dd9ffe7b4729febe48 e7fdc662d6305fee2908c3f1630e0b20d6f4689a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'evolve', 'user': 'test'}
  11f849d7159fa30a63dbbc1a6d251a8d996baeb5 e7fdc662d6305fee2908c3f1630e0b20d6f4689a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'evolve', 'user': 'test'}
  ca1b80f7960aae2306287bab52b4090c59af8c29 e2ce33033e42db2e61a5f71c6dfb52a33efeaf6a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  c41c793e0ef1ddb463e85ea9491e377d01127ba2 be5a8b9faa8af54f115aa168a2c8564acb40c37d 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  801b5920c7ea8d4ebdbc9cfc1e79e665dea2f211 5cf74a13db180e33dc2df8cd2aa70b21252a2a64 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '73', 'operation': 'amend', 'user': 'test'}
  801b5920c7ea8d4ebdbc9cfc1e79e665dea2f211 45e15d6e88f5bd23ba360dff0c7591eca2d99f43 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  5cf74a13db180e33dc2df8cd2aa70b21252a2a64 911c21adca136894a2b35f0a58fae7ee94fa5e61 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  911c21adca136894a2b35f0a58fae7ee94fa5e61 618f8bd245a8d1892954eb49a88a6ec5e500a5b5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'evolve', 'user': 'test'}
  45e15d6e88f5bd23ba360dff0c7591eca2d99f43 618f8bd245a8d1892954eb49a88a6ec5e500a5b5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '73', 'operation': 'evolve', 'user': 'test'}
  $ hg obslog --all
  @    618f8bd245a8 (15) added foo to x
  |\     rewritten(description, branch, content) from 45e15d6e88f5 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |    rewritten from 911c21adca13 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  45e15d6e88f5 (13) added x
  | |    rebased(parent) from 801b5920c7ea using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  911c21adca13 (14) added foo to x
  | |    rebased(parent) from 5cf74a13db18 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  5cf74a13db18 (12) added foo to x
  |/     rewritten(description, branch, content) from 801b5920c7ea using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  801b5920c7ea (11) added x
  

Testing when both the content-divergence are on different parents and resolution
will lead to conflicts
---------------------------------------------------------------------------------

  $ hg up .^^^
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved

  $ echo y > y
  $ hg ci -Aqm "added y"
  $ hg glog -r .
  @  16:ecf1d3992eb4 added y
  |   () [default] draft
  ~

  $ echo bar > y
  $ hg amend

  $ hg up 'predecessors(.)' --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset ecf1d3992eb4
  (hidden revision 'ecf1d3992eb4' was rewritten as: 9c32d35206fb)
  working directory parent is obsolete! (ecf1d3992eb4)
  (use 'hg evolve' to update to its successor: 9c32d35206fb)
  $ hg rebase -r . -d 'desc("added foo to x")' --config experimental.evolution.allowdivergence=True
  rebasing 16:ecf1d3992eb4 "added y"
  2 new content-divergent changesets
  $ echo wat > y
  $ hg amend

  $ hg glog
  @  19:bfe170c9c964 added y
  |   () [bar] draft
  | *  17:9c32d35206fb added y
  | |   () [default] draft
  o |  15:618f8bd245a8 added foo to x
  | |   () [bar] draft
  o |  10:be5a8b9faa8a added d
  | |   () [default] draft
  o |  9:e2ce33033e42 added c
  |/    () [default] draft
  o  8:e7fdc662d630 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[17] added y
  with: [19] added y
  base: [16] added y
  rebasing "divergent" content-divergent changeset 9c32d35206fb on 618f8bd245a8
  merging y
  warning: conflicts while merging y! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [1]

  $ echo watbar > y
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue
  $ hg evolve --continue
  working directory is now at 7411ed2cf7cf

  $ hg glog
  @  21:7411ed2cf7cf added y
  |   () [bar] draft
  o  15:618f8bd245a8 added foo to x
  |   () [bar] draft
  o  10:be5a8b9faa8a added d
  |   () [default] draft
  o  9:e2ce33033e42 added c
  |   () [default] draft
  o  8:e7fdc662d630 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg debugobsolete
  b1661037fa25511d0b7ccddf405e336f9d7d3424 7ed0642d644bb9ad93d252dd9ffe7b4729febe48 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  b1661037fa25511d0b7ccddf405e336f9d7d3424 da4b96f4a8d610a85b225583138f681d67e275dd 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  da4b96f4a8d610a85b225583138f681d67e275dd 11f849d7159fa30a63dbbc1a6d251a8d996baeb5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7ed0642d644bb9ad93d252dd9ffe7b4729febe48 e7fdc662d6305fee2908c3f1630e0b20d6f4689a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'evolve', 'user': 'test'}
  11f849d7159fa30a63dbbc1a6d251a8d996baeb5 e7fdc662d6305fee2908c3f1630e0b20d6f4689a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'evolve', 'user': 'test'}
  ca1b80f7960aae2306287bab52b4090c59af8c29 e2ce33033e42db2e61a5f71c6dfb52a33efeaf6a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  c41c793e0ef1ddb463e85ea9491e377d01127ba2 be5a8b9faa8af54f115aa168a2c8564acb40c37d 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  801b5920c7ea8d4ebdbc9cfc1e79e665dea2f211 5cf74a13db180e33dc2df8cd2aa70b21252a2a64 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '73', 'operation': 'amend', 'user': 'test'}
  801b5920c7ea8d4ebdbc9cfc1e79e665dea2f211 45e15d6e88f5bd23ba360dff0c7591eca2d99f43 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  5cf74a13db180e33dc2df8cd2aa70b21252a2a64 911c21adca136894a2b35f0a58fae7ee94fa5e61 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  911c21adca136894a2b35f0a58fae7ee94fa5e61 618f8bd245a8d1892954eb49a88a6ec5e500a5b5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'evolve', 'user': 'test'}
  45e15d6e88f5bd23ba360dff0c7591eca2d99f43 618f8bd245a8d1892954eb49a88a6ec5e500a5b5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '73', 'operation': 'evolve', 'user': 'test'}
  ecf1d3992eb4d9700d441013fc4e89014692b461 9c32d35206fb5c3bf0ac814d410914d54a959a87 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  ecf1d3992eb4d9700d441013fc4e89014692b461 491e9c6e22a4f265fad54d2060b9c2fa45f4301d 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '68', 'operation': 'rebase', 'user': 'test'}
  491e9c6e22a4f265fad54d2060b9c2fa45f4301d bfe170c9c96484157a071cd74e400426376c5e0e 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  9c32d35206fb5c3bf0ac814d410914d54a959a87 7c47d5c3b6f5fb934723cdeb45c5819760988e1d 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7c47d5c3b6f5fb934723cdeb45c5819760988e1d 7411ed2cf7cfbc23f17711a72570787569177d69 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '72', 'operation': 'evolve', 'user': 'test'}
  bfe170c9c96484157a071cd74e400426376c5e0e 7411ed2cf7cfbc23f17711a72570787569177d69 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'evolve', 'user': 'test'}
  $ hg obslog -r . --all
  @    7411ed2cf7cf (21) added y
  |\     rewritten(branch, content) from 7c47d5c3b6f5 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |    amended(content) from bfe170c9c964 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  7c47d5c3b6f5 (20) added y
  | |    rebased(parent) from 9c32d35206fb using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  bfe170c9c964 (19) added y
  | |    amended(content) from 491e9c6e22a4 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  491e9c6e22a4 (18) added y
  | |    rewritten(branch, parent) from ecf1d3992eb4 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  9c32d35206fb (17) added y
  |/     amended(content) from ecf1d3992eb4 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  ecf1d3992eb4 (16) added y
  

checking that relocated commit is there
  $ hg exp 20 --hidden
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 7c47d5c3b6f5fb934723cdeb45c5819760988e1d
  # Parent  618f8bd245a8d1892954eb49a88a6ec5e500a5b5
  added y
  
  diff -r 618f8bd245a8 -r 7c47d5c3b6f5 y
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +bar

Testing when the relocation will result in conflicts and merging also:
----------------------------------------------------------------------

  $ hg glog
  @  21:7411ed2cf7cf added y
  |   () [bar] draft
  o  15:618f8bd245a8 added foo to x
  |   () [bar] draft
  o  10:be5a8b9faa8a added d
  |   () [default] draft
  o  9:e2ce33033e42 added c
  |   () [default] draft
  o  8:e7fdc662d630 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg up .^^^^
  0 files updated, 0 files merged, 4 files removed, 0 files unresolved

  $ echo z > z
  $ hg ci -Aqm "added z"
  $ hg glog -r .
  @  22:2048a66e8834 added z
  |   () [default] draft
  ~

  $ echo foo > y
  $ hg add y
  $ hg amend

  $ hg up 'predecessors(.)' --hidden
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  updated to hidden changeset 2048a66e8834
  (hidden revision '2048a66e8834' was rewritten as: 9bc2ace42175)
  working directory parent is obsolete! (2048a66e8834)
  (use 'hg evolve' to update to its successor: 9bc2ace42175)
  $ hg rebase -r . -d 'desc("added y")' --config experimental.evolution.allowdivergence=True
  rebasing 22:2048a66e8834 "added z"
  2 new content-divergent changesets
  $ echo bar > z
  $ hg amend

  $ hg glog
  @  25:40a21b3496bc added z
  |   () [bar] draft
  | *  23:9bc2ace42175 added z
  | |   () [default] draft
  o |  21:7411ed2cf7cf added y
  | |   () [bar] draft
  o |  15:618f8bd245a8 added foo to x
  | |   () [bar] draft
  o |  10:be5a8b9faa8a added d
  | |   () [default] draft
  o |  9:e2ce33033e42 added c
  |/    () [default] draft
  o  8:e7fdc662d630 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent --any
  merge:[23] added z
  with: [25] added z
  base: [22] added z
  rebasing "divergent" content-divergent changeset 9bc2ace42175 on 7411ed2cf7cf
  merging y
  warning: conflicts while merging y! (edit, then use 'hg resolve --mark')
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [1]

  $ hg diff
  diff -r 7411ed2cf7cf y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< destination: 7411ed2cf7cf bar - test: added y
   watbar
  +=======
  +foo
  +>>>>>>> evolving:    9bc2ace42175 - test: added z
  diff -r 7411ed2cf7cf z
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/z	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +z

  $ echo foo > y
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  evolving 23:9bc2ace42175 "added z"
  merging y
  warning: conflicts while merging y! (edit, then use 'hg resolve --mark')
  1 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [1]

  $ hg diff
  diff -r 635c0edd2e45 y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< local: 635c0edd2e45 - test: added z
   foo
  +=======
  +watbar
  +>>>>>>> other: 40a21b3496bc bar - test: added z
  diff -r 635c0edd2e45 z
  --- a/z	Thu Jan 01 00:00:00 1970 +0000
  +++ b/z	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -z
  +bar

  $ echo foo > y
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue
  $ hg evolve --continue
  working directory is now at 664febd074c2

  $ hg glog
  @  27:664febd074c2 added z
  |   () [bar] draft
  o  21:7411ed2cf7cf added y
  |   () [bar] draft
  o  15:618f8bd245a8 added foo to x
  |   () [bar] draft
  o  10:be5a8b9faa8a added d
  |   () [default] draft
  o  9:e2ce33033e42 added c
  |   () [default] draft
  o  8:e7fdc662d630 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Branch bar
  # Node ID 664febd074c2f9c5c4e03045dd688e93360f297c
  # Parent  7411ed2cf7cfbc23f17711a72570787569177d69
  added z
  
  diff -r 7411ed2cf7cf -r 664febd074c2 y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -watbar
  +foo
  diff -r 7411ed2cf7cf -r 664febd074c2 z
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/z	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +bar

  $ hg debugobsolete
  b1661037fa25511d0b7ccddf405e336f9d7d3424 7ed0642d644bb9ad93d252dd9ffe7b4729febe48 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  b1661037fa25511d0b7ccddf405e336f9d7d3424 da4b96f4a8d610a85b225583138f681d67e275dd 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  da4b96f4a8d610a85b225583138f681d67e275dd 11f849d7159fa30a63dbbc1a6d251a8d996baeb5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7ed0642d644bb9ad93d252dd9ffe7b4729febe48 e7fdc662d6305fee2908c3f1630e0b20d6f4689a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'evolve', 'user': 'test'}
  11f849d7159fa30a63dbbc1a6d251a8d996baeb5 e7fdc662d6305fee2908c3f1630e0b20d6f4689a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'evolve', 'user': 'test'}
  ca1b80f7960aae2306287bab52b4090c59af8c29 e2ce33033e42db2e61a5f71c6dfb52a33efeaf6a 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  c41c793e0ef1ddb463e85ea9491e377d01127ba2 be5a8b9faa8af54f115aa168a2c8564acb40c37d 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  801b5920c7ea8d4ebdbc9cfc1e79e665dea2f211 5cf74a13db180e33dc2df8cd2aa70b21252a2a64 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '73', 'operation': 'amend', 'user': 'test'}
  801b5920c7ea8d4ebdbc9cfc1e79e665dea2f211 45e15d6e88f5bd23ba360dff0c7591eca2d99f43 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  5cf74a13db180e33dc2df8cd2aa70b21252a2a64 911c21adca136894a2b35f0a58fae7ee94fa5e61 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  911c21adca136894a2b35f0a58fae7ee94fa5e61 618f8bd245a8d1892954eb49a88a6ec5e500a5b5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'evolve', 'user': 'test'}
  45e15d6e88f5bd23ba360dff0c7591eca2d99f43 618f8bd245a8d1892954eb49a88a6ec5e500a5b5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '73', 'operation': 'evolve', 'user': 'test'}
  ecf1d3992eb4d9700d441013fc4e89014692b461 9c32d35206fb5c3bf0ac814d410914d54a959a87 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  ecf1d3992eb4d9700d441013fc4e89014692b461 491e9c6e22a4f265fad54d2060b9c2fa45f4301d 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '68', 'operation': 'rebase', 'user': 'test'}
  491e9c6e22a4f265fad54d2060b9c2fa45f4301d bfe170c9c96484157a071cd74e400426376c5e0e 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  9c32d35206fb5c3bf0ac814d410914d54a959a87 7c47d5c3b6f5fb934723cdeb45c5819760988e1d 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7c47d5c3b6f5fb934723cdeb45c5819760988e1d 7411ed2cf7cfbc23f17711a72570787569177d69 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '72', 'operation': 'evolve', 'user': 'test'}
  bfe170c9c96484157a071cd74e400426376c5e0e 7411ed2cf7cfbc23f17711a72570787569177d69 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'evolve', 'user': 'test'}
  2048a66e8834bda866dcc8c479f091897816833e 9bc2ace42175da7380251fca97730f62ff5b9185 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  2048a66e8834bda866dcc8c479f091897816833e 8bf0130be95ef72377e39232335531426c2abcf9 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '68', 'operation': 'rebase', 'user': 'test'}
  8bf0130be95ef72377e39232335531426c2abcf9 40a21b3496bc55fd0c0ac92d81b2930cfa4d4bef 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  9bc2ace42175da7380251fca97730f62ff5b9185 635c0edd2e45de215b2061b30aae5168708238d3 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '12', 'operation': 'evolve', 'user': 'test'}
  635c0edd2e45de215b2061b30aae5168708238d3 664febd074c2f9c5c4e03045dd688e93360f297c 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '72', 'operation': 'evolve', 'user': 'test'}
  40a21b3496bc55fd0c0ac92d81b2930cfa4d4bef 664febd074c2f9c5c4e03045dd688e93360f297c 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'evolve', 'user': 'test'}
  $ hg obslog --all
  @    664febd074c2 (27) added z
  |\     amended(content) from 40a21b3496bc using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |    rewritten(branch, content) from 635c0edd2e45 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  40a21b3496bc (25) added z
  | |    amended(content) from 8bf0130be95e using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  635c0edd2e45 (26) added z
  | |    rewritten(parent, content) from 9bc2ace42175 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  8bf0130be95e (24) added z
  | |    rewritten(branch, parent) from 2048a66e8834 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  9bc2ace42175 (23) added z
  |/     amended(content) from 2048a66e8834 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  2048a66e8834 (22) added z
  

  $ cd ..

Testing when relocation results in nothing to commit
----------------------------------------------------

Set up a repo where relocation results in no changes to commit because the
changes from the relocated node are already in the destination.

  $ hg init nothing-to-commit
  $ cd nothing-to-commit
  $ echo 0 > a
  $ hg ci -Aqm initial
  $ echo 1 > a
  $ hg ci -Aqm upstream
  $ hg prev -q

Create the source of divergence.
  $ echo 0 > b
  $ hg ci -Aqm divergent

The first side of the divergence get rebased on top of upstream.
  $ hg rebase -r . -d 'desc("upstream")'
  rebasing 2:898ddd4443b3 "divergent" (tip)
  $ hg --hidden co 2 -q
  updated to hidden changeset 898ddd4443b3
  (hidden revision '898ddd4443b3' was rewritten as: befae6138569)
  working directory parent is obsolete! (898ddd4443b3)

The other side of the divergence gets amended so it matches upstream.
Relocation (onto upstream) will therefore result in no changes to commit.
  $ hg revert -r 'desc("upstream")' --all
  removing b
  reverting a
  $ hg amend --config experimental.evolution.allowdivergence=True
  2 new content-divergent changesets

Add a commit on top. This one should become an orphan. Evolving it later
should put it on top of the other divergent side (the one that's on top of
upstream)
  $ echo 0 > c
  $ hg ci -Aqm child
  $ hg co -q null
  $ hg glog
  o  5:88473f9137d1 child
  |   () [default] draft
  *  4:4cc21313ecee divergent
  |   () [default] draft
  | *  3:befae6138569 divergent
  | |   () [default] draft
  | o  1:33c576d20069 upstream
  |/    () [default] draft
  o  0:98a3f8f02ba7 initial
      () [default] draft
  $ hg evolve --content-divergent
  merge:[3] divergent
  with: [4] divergent
  base: [2] divergent
  rebasing "other" content-divergent changeset 4cc21313ecee on 33c576d20069
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  1 new orphan changesets
  $ hg glog
  o  7:cc3d0c6117c7 divergent
  |   () [default] draft
  | *  5:88473f9137d1 child
  | |   () [default] draft
  | x  4:4cc21313ecee divergent
  | |   () [default] draft
  o |  1:33c576d20069 upstream
  |/    () [default] draft
  o  0:98a3f8f02ba7 initial
      () [default] draft

  $ hg evolve --any
  move:[5] child
  atop:[7] divergent
  $ hg glog
  o  8:916b4ec3b91f child
  |   () [default] draft
  o  7:cc3d0c6117c7 divergent
  |   () [default] draft
  o  1:33c576d20069 upstream
  |   () [default] draft
  o  0:98a3f8f02ba7 initial
      () [default] draft
  $ hg debugobsolete
  898ddd4443b3d5520bf48f22f9411d5a0751cf2e befae61385695f1ae4b78b030ad91075b2b523ef 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  898ddd4443b3d5520bf48f22f9411d5a0751cf2e 4cc21313ecee97ce33265514a0596a192bfa6b3f 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  4cc21313ecee97ce33265514a0596a192bfa6b3f bf4fe3a3afeb14c338094f41a35863921856592f 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '12', 'operation': 'evolve', 'user': 'test'}
  befae61385695f1ae4b78b030ad91075b2b523ef cc3d0c6117c7400995107497370fa4c2138399cd 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'evolve', 'user': 'test'}
  bf4fe3a3afeb14c338094f41a35863921856592f cc3d0c6117c7400995107497370fa4c2138399cd 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'evolve', 'user': 'test'}
  88473f9137d12e90055d30bbb9b78dd786520870 916b4ec3b91fd03826bd4b179051ae3cee633b56 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  $ hg obslog -r 'desc("divergent")' --all
  o    cc3d0c6117c7 (7) divergent
  |\     amended(content) from befae6138569 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |    rewritten from bf4fe3a3afeb using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  befae6138569 (3) divergent
  | |    rebased(parent) from 898ddd4443b3 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  bf4fe3a3afeb (6) divergent
  | |    rewritten(parent, content) from 4cc21313ecee using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  4cc21313ecee (4) divergent
  |/     amended(content) from 898ddd4443b3 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  898ddd4443b3 (2) divergent
  
  $ cd ..
